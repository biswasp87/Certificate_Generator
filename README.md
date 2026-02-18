# Certificate Generator

A Python-based web application to generate certificates by mapping Excel data onto image templates.

## Features
- **Excel Data Upload**: Upload `.xlsx` or `.xls` files.
- **Hindi/English Column Mapping**: Mark specific columns as Hindi data via a modal.
- **Template Management**: Upload template images and up to 4 signature images.
- **Interactive Preview Pane**:
  - Drag and drop fields onto the certificate template.
  - Three-column layout: English fields (left), Preview (center), Hindi fields (right).
- **Customization**:
  - Adjust font size for each field.
  - Select from custom fonts stored in `fonts/Hindi Font` and `fonts/English Font`.
- **Persistence**: Save template configurations (positions, fonts) to a local SQLite database.

## Project Structure
- `app.py`: Flask backend with API endpoints.
- `models.py`: SQLAlchemy database models.
- `templates/index.html`: Vue.js frontend with Tailwind CSS and Interact.js.
- `uploads/`: Stores uploaded templates and signatures.
- `fonts/`: Folders for Hindi and English fonts.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

3. **Font Setup**:
   Place your `.ttf` or `.otf` font files in the corresponding folders:
   - `fonts/Hindi Font/`
   - `fonts/English Font/`

## Usage
1. Open the application.
2. Upload an Excel file.
3. In the modal, mark which columns contain Hindi data.
4. Upload or select a certificate template.
5. Click on English/Hindi fields on the sidebars to add them to the template.
6. Drag the fields to your desired position.
7. Use the controls to adjust font size and font family.
8. Settings are automatically saved as you make changes.
