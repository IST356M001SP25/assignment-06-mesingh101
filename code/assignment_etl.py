import streamlit as st
import pandas as pd
import requests
import json

# file: code/assignment_etl.py

PLACE_IDS_FILE = "cache/place_ids.csv"
CACHE_REVIEWS_FILE = "cache/reviews.csv"
CACHE_SENTIMENT_FILE = "cache/reviews_sentiment_by_sentence.csv"
CACHE_ENTITIES_FILE = "cache/reviews_sentiment_by_sentence_with_entities.csv"


if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition
else:
    from code.apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition


def reviews_step(place_ids: str | pd.DataFrame) -> pd.DataFrame:
    """Step 1: Get reviews for each Google Place ID."""
    if isinstance(place_ids, str):
        place_ids_df = pd.read_csv(place_ids)
    else:
        place_ids_df = place_ids

    all_places = []
    for _, row in place_ids_df.iterrows():
        details = get_google_place_details(row['Google Place ID'])
        all_places.append(details['result'])

    reviews_df = pd.json_normalize(
        all_places, record_path='reviews', meta=['place_id', 'name']
    )

    reviews_df = reviews_df[['place_id', 'name', 'author_name', 'rating', 'text']]
    reviews_df.to_csv(REVIEWS_FILE, index=False)
    return reviews_df

def sentiment_step(reviews: str | pd.DataFrame) -> pd.DataFrame:
    """Step 2: Get sentence-level sentiment analysis for each review."""
    if isinstance(reviews, str):
        reviews_df = pd.read_csv(reviews)
    else:
        reviews_df = reviews

    sentiment_data = []
    for _, row in reviews_df.iterrows():
        result = get_azure_sentiment(row['text'])
        doc = result['results']['documents'][0]
        doc.update({
            'place_id': row['place_id'],
            'name': row['name'],
            'author_name': row['author_name'],
            'rating': row['rating']
        })
        sentiment_data.append(doc)

    sentiment_df = pd.json_normalize(
        sentiment_data, record_path='sentences', meta=['place_id', 'name', 'author_name', 'rating']
    )

    sentiment_df.rename(columns={
        'text': 'sentence_text',
        'sentiment': 'sentence_sentiment'
    }, inplace=True)

    sentiment_df = sentiment_df[[
        'place_id', 'name', 'author_name', 'rating',
        'sentence_text', 'sentence_sentiment',
        'confidenceScores.positive', 'confidenceScores.neutral', 'confidenceScores.negative'
    ]]

    sentiment_df.to_csv(SENTIMENT_FILE, index=False)
    return sentiment_df

def entity_extraction_step(sentiments: str | pd.DataFrame) -> pd.DataFrame:
    """Step 3: Extract named entities from each sentence."""
    if isinstance(sentiments, str):
        sentiment_df = pd.read_csv(sentiments)
    else:
        sentiment_df = sentiments

    entity_rows = []
    for _, row in sentiment_df.iterrows():
        response = get_azure_named_entity_recognition(row['sentence_text'])
        entities = response['results']['documents'][0]['entities']
        for entity in entities:
            record = row.to_dict()
            record.update({
                'entity_text': entity.get('text'),
                'entity_category': entity.get('category'),
                'entity_subcategory': entity.get('subcategory', ''),
                'confidenceScores.entity': entity.get('confidenceScore')
            })
            entity_rows.append(record)

    final_df = pd.DataFrame(entity_rows)
    final_df.to_csv(ENTITIES_FILE, index=False)
    return final_df

# Run everything with Streamlit for debugging
if __name__ == "__main__":
    reviews = reviews_step(PLACE_IDS_FILE)
    sentiments = sentiment_step(REVIEWS_FILE)
    entities = entity_extraction_step(SENTIMENT_FILE)
    st.dataframe(entities)
