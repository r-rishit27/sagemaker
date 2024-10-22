
# SageMaker - Make Anything Bot

**AI-Powered Creation Assistance Platform**

The **SageMaker-Make Anything Bot** is an AI-powered platform designed to streamline the process of creating projects by providing users with personalized step-by-step guidance, smart material recommendations, and curated tutorial videos. Leveraging **Google Gemini Vision Pro**, **Python Django**, and **Generative AI**, this tool reduces search time, improves user engagement, and enhances the overall creation experience.

Video Demo link : https://youtu.be/Vm9a1Mh63VU

![Alt text](https://github.com/r-rishit27/sagemaker/blob/main/sagarch.jpg)

## Features

- **Personalized Step-by-Step Guidance:**  
  The bot provides users with detailed instructions tailored to their specific projects, ensuring smooth workflows and reducing confusion.

- **Smart Material Recommendations:**  
  Uses **Generative AI** and **vector databases** to recommend the best materials and tools based on user input, optimizing the creation process.

- **Dynamic Cart Integration:**  
  Automatically adds the required items to the user's cart, minimizing the chance of missing out on necessary materials.

- **Video Tutorials & Support:**  
  Offers curated tutorial videos to guide users through the entire process, ensuring they have the resources needed to complete their projects.

- **Real-Time API Integration:**  
  Integrates with live APIs to adapt to user preferences and provide updated recommendations, ensuring a personalized experience.

- **Creative Empowerment:**  
  Empowers users to turn their ideas into reality, enhancing engagement by an estimated 30% and boosting project completion rates.

## Technology Stack

- **Frontend:**  
  - **Streamlit:** For an interactive and user-friendly interface.
  
- **Backend:**  
  - **Django & JavaScript:** Powering robust data handling and dynamic functionalities.
  - **SQL Database:** Efficient data management for user projects, materials, and recommendations.
  
- **AI/ML Technologies:**
  - **Google Gemini 1.5 Pro Vision LLM**: For enhanced natural language understanding and product/material recognition.
  - **Hugging Face Word Embeddings**: Enabling similarity search and context-aware recommendations.
  - **ChromaDB**: For storing and searching vectorized data efficiently.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/sagemaker.git
2.Install dependencies:
   ```bash
    
    pip install -r requirements.txt

3.Set up environment variables in a .env file:
   ```bash
    touch .enV
   
4.Run the Streamlit application:
   ```bash
  streamlit run app.py


