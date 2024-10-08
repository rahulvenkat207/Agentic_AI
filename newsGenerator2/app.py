import streamlit as st
from crew import NewsletterGenCrew

class NewsletterGenUI:

    def load_html_template(self):
        with open("C:/secuqrprograms/original/newsretriever/newsletter_template.html", "r") as file:
            html_template = file.read()
        return html_template

    def generate_newsletter(self, topic, personal_message):
        inputs = {
            "personal_message": personal_message,
            "html_template": self.load_html_template(),
        }
        # Generate the newsletter and ensure it is converted to HTML or plain text
        result = NewsletterGenCrew().crew().kickoff(inputs=inputs)
        return result

    def newsletter_generation(self):

        if st.session_state.generating:
            st.session_state.newsletter = self.generate_newsletter(
                 st.session_state.personal_message
            )

        if st.session_state.newsletter and st.session_state.newsletter != "":
            with st.container():
                st.write("Newsletter generated successfully!")

                # Ensure the newsletter content is in HTML format
                if isinstance(st.session_state.newsletter, str):
                    newsletter_html = st.session_state.newsletter
                else:
                    # Convert to string if it's not already in string format
                    newsletter_html = str(st.session_state.newsletter)  # Adjust if necessary

                st.download_button(
                    label="Download HTML file",
                    data=newsletter_html,
                    file_name="newsletter.html",
                    mime="text/html",
                )
            st.session_state.generating = False

    def sidebar(self):
        with st.sidebar:
            st.title("Newsletter Generator")

            st.write(
                """
                To generate a newsletter, enter a topic and a personal message. \n
                Your team of AI agents will generate a newsletter for you!
                """
            )


            st.text_area(
                "Your personal message (to include at the top of the newsletter)",
                key="personal_message",
                placeholder="Dear readers, welcome to the newsletter!",
            )

            if st.button("Generate Newsletter"):
                st.session_state.generating = True

    def render(self):
        st.set_page_config(page_title="Newsletter Generation", page_icon="📧")

       

        if "personal_message" not in st.session_state:
            st.session_state.personal_message = ""

        if "newsletter" not in st.session_state:
            st.session_state.newsletter = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()
        self.newsletter_generation()

if __name__ == "__main__":
    NewsletterGenUI().render()
