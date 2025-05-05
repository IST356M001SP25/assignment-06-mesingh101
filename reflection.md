# Reflection

Student Name:  Mera Singh
Sudent Email:  mesingh@syr.edu

## Instructions

Reflection is a key activity of learning. It helps you build a strong metacognition, or "understanding of your own learning." A good learner not only "knows what they know", but they "know what they don't know", too. Learning to reflect takes practice, but if your goal is to become a self-directed learner where you can teach yourself things, reflection is imperative.

- Now that you've completed the assignment, share your throughts. What did you learn? What confuses you? Where did you struggle? Where might you need more practice?
- A good reflection is: **specific as possible**,  **uses the terminology of the problem domain** (what was learned in class / through readings), and **is actionable** (you can pursue next steps, or be aided in the pursuit). That last part is what will make you a self-directed learner.
- Flex your recall muscles. You might have to review class notes / assigned readings to write your reflection and get the terminology correct.
- Your reflection is for **you**. Yes I make you write them and I read them, but you are merely practicing to become a better self-directed learner. If you read your reflection 1 week later, does what you wrote advance your learning?

Examples:

- **Poor Reflection:**  "I don't understand loops."   
**Better Reflection:** "I don't undersand how the while loop exits."   
**Best Reflection:** "I struggle writing the proper exit conditions on a while loop." It's actionable: You can practice this, google it, ask Chat GPT to explain it, etc. 
-  **Poor Reflection** "I learned loops."   
**Better Reflection** "I learned how to write while loops and their difference from for loops."   
**Best Reflection** "I learned when to use while vs for loops. While loops are for sentiel-controlled values (waiting for a condition to occur), vs for loops are for iterating over collections of fixed values."

`--- Reflection Below This Line ---`

I still couldn’t get the full pipeline to work, but I did make progress on understanding how multi-step ETL processes function using APIs. I was able to successfully implement and test individual API calls for Google Places and Azure services (like sentiment analysis and entity recognition). However, I struggled with the file pathing and understanding exactly how the caching and CSV outputs were being saved and read. My main issue was making sure that the files (like cache/reviews.csv) were being generated properly, and then picked up by the tests.

I understand the concept of transforming data through multiple stages (place → review → sentiment → entities), but I need more practice with debugging file I/O errors in Python and understanding the structure of the test environment — especially how files need to be created ahead of time for tests to pass.

For next steps, I plan to review the use of os.path and __main__ blocks in Python scripts, and get more hands-on experience running scripts that generate output used by other modules or tests. I’ll also look into how to verify file paths dynamically to avoid hardcoded assumptions that may break.

