# ExamTimer Pro

A projector-friendly Streamlit timer for examinations and classroom assessments.

## Features
- Large countdown with 3D-style circular progress ring
- Adjustable reading and writing times
- Green, amber, red and flashing final stages
- Start, pause, resume, reset and ±1 minute controls
- Full-screen projector mode
- Configurable milestone messages and browser-generated sound
- Optional logo, title and subtitle
- Midnight, Light and Slate themes
- No preset exam-type buttons

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository.
2. Upload the contents of this folder to the repository root.
3. Create a new app in Streamlit Community Cloud.
4. Select `app.py` as the main file and deploy.

## Important exam-use notes
- Test the projector, sound and full-screen mode before the assessment.
- Keep the presenting computer connected to power and disable sleep.
- Sound and full-screen mode require a user click because of browser security rules.
- The countdown uses the browser clock, so it continues accurately if rendering is briefly delayed.

## Keyboard shortcuts
- `Space`: start or pause
- `F`: full screen
- `R`: reset
