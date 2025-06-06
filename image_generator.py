import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

st.title("Image generated with Google GenAI")
st.markdown("This app generates images based on your prompts using Google GenAI:")

contents = st.text_area("Enter your text here:", height=100)

if st.button("Generate Image", type="primary"):
    if not contents:
        st.error("Please enter a text prompt.")
    else:
        with st.spinner("Generating Image..."):
            try:
                client = genai.Client(api_key="AIzaSyB1Bk1rBDni2UGQ9TGNZjkvvauCcBVTSuo")  
                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )
                if response.candidates and len(response.candidates) > 0:
                    text_found = False
                    image_found = False
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, "text") and part.text is not None:
                            st.markdown("### Model Response")
                            st.write(part.text)
                            text_found = True
                        elif hasattr(part, "inline_data") and part.inline_data is not None:
                            try:
                                image = Image.open(BytesIO(part.inline_data.data))
                                st.markdown("### Generated Image")
                                st.image(image, caption="Generated Image", use_container_width=True)

                                image.save("gemini-native-image.png")
                                img_buffer = BytesIO()
                                image.save(img_buffer, format="PNG")
                                img_buffer.seek(0)

                                st.download_button(
                                    label="Download Image",
                                    data=img_buffer.getvalue(),
                                    file_name="gemini-native-image.png",
                                    mime="image/png"
                                )
                                image_found = True
                                st.success("Image generated successfully!")
                            except Exception as e:
                                st.error(f"Error processing image: {e}")
                    if not text_found and not image_found:
                        st.warning("No text or image found in the response.")
                else:
                    st.error("No response from the model.")
            except Exception as e:
                st.error(f"An error occurred while generating content: {e}")

with st.expander("About"):
    st.markdown("""
    This application uses Google GenAI to generate images based on user-provided text prompts.
    It allows users to input a prompt and receive a generated image in response.

    **Note:** Ensure you have the necessary API key and permissions to use Google GenAI services.
    """)
