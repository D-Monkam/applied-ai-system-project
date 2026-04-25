import streamlit as st
from pawpal_system import Owner, Pet
from pet_care_advisor import PetCareAdvisor
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="PetCare AI", page_icon="🐾", layout="centered")

st.title("🐾 PetCare AI")

st.markdown(
    """
Welcome to PetCareAI, your AI-powered pet care advisor.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PetCare AI** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

st.divider()

st.subheader("Owner Details")
owner_name = st.text_input("Owner name", value="Jordan")

# Initialize owner in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
else:
    st.session_state.owner.name = owner_name

# --- AI Advisor Initialization ---
# Define the paths for the knowledge base
KNOWLEDGE_BASE_PATHS = ["knowledge_base", "uploads"]

# Use st.cache_resource to load the model only once
@st.cache_resource
def get_advisor(_owner):
    # Pass the owner object and the list of paths to the advisor
    return PetCareAdvisor(knowledge_base_path=KNOWLEDGE_BASE_PATHS, owner=_owner)

# Get the advisor instance
advisor = get_advisor(st.session_state.owner)

# --- Pet Management ---
st.markdown("### Your Pets")
with st.form("add_pet_form"):
    c1, c2 = st.columns(2)
    with c1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with c2:
        species = st.selectbox("Species", ["dog", "cat", "other"], help="The pet's species (e.g., dog, cat).")
    
    age = st.number_input("Age", min_value=0, max_value=30, value=1, step=1)
    general_info = st.text_area("Additional Info", placeholder="e.g., Loves squeaky toys, has a sensitive stomach, gets anxious during thunderstorms.")

    submitted = st.form_submit_button("Add Pet")
    if submitted and pet_name:
        new_pet = Pet(name=pet_name, breed=species, age=age, general_info=general_info)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {pet_name} to your family!")
        st.rerun()

if st.session_state.owner.pets:
    pet_choices = {pet.name: pet for pet in st.session_state.owner.pets}
    selected_pet_name = st.selectbox("Select a pet", options=list(pet_choices.keys()))
    st.session_state.selected_pet = pet_choices[selected_pet_name]
    st.write(f"Current pets: {', '.join([pet.name for pet in st.session_state.owner.pets])}")
else:
    st.info("No pets added yet. Add one above to get started!")
    st.session_state.selected_pet = None

st.divider()

# --- File Uploader for Custom Knowledge ---
st.subheader("📚 Add to Knowledge Base")
st.caption("Upload .txt files to add more knowledge for the advisor to use.")

uploaded_files = st.file_uploader(
    "Choose .txt files", accept_multiple_files=True, type="txt"
)

if uploaded_files:
    # Create the uploads directory if it doesn't exist
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    for uploaded_file in uploaded_files:
        # Write the uploaded file to the uploads directory
        with open(os.path.join(uploads_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    st.success(f"Successfully saved {len(uploaded_files)} file(s).")

# Add a button to allow the user to manually reload the advisor
if st.button("Reload Advisor with New Knowledge"):
    # Clear the cached resource
    get_advisor.clear()
    st.success("Advisor has been reloaded with the new knowledge!")
    # Rerun the script to instantiate the advisor again
    st.rerun()

st.divider()

# --- AI Pet Care Advisor ---
st.subheader("🤖 Ask the PetCare Advisor")
st.caption("Ask a question about pet care. If you mention your pet's name, the advisor will use their details in its answer!")

question = st.text_input("Your question", placeholder="e.g., How can I keep my cat Mochi entertained?")

if st.button("Get Advice"):
    if question:
        with st.spinner("The PetCare Advisor is thinking..."):
            result = advisor.ask(question)
            
            if "error" in result:
                st.error(result["error"])
            else:
                st.markdown(result["answer"])
                if result.get("source_documents"):
                    sources = ", ".join(result["source_documents"])
                    st.info(f"💡 This answer was informed by the following documents: {sources}")
    else:
        st.warning("Please enter a question.")
