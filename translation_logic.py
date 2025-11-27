from docx import Document as doc
from docxlatex import Document as docxlatex
from tkinter import filedialog
file_path = filedialog.askopenfilename()
#save_path = filedialog.asksaveasfilename()
docxlatex = docxlatex(file_path)
doc = doc(file_path)
from deep_translator import GoogleTranslator
from docx.oxml.ns import nsdecls
from lxml import etree

# Define the common XML namespaces for easier reading
W_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
M_NAMESPACE = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
WP_NAMESPACE = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'


def trans_case1():
    for table in doc.tables:
        # Use enumerate to get both the index (r_count) and the item (row)
        for r_count, row in enumerate(table.rows):
            # Reset column count for each new row
            for c_count, cell in enumerate(row.cells):
                if r_count != 0 and r_count !=7 and c_count ==0:
                    next_cell = row.cells[c_count+1]
                    next_cell.text = GoogleTranslator(source='auto', target='en').translate(cell.text)
                    print(cell.text)
                    print(f"Table, Row {r_count}, Col {c_count}")
                    print(next_cell.text)
                else:
                    pass

def trans_case2():
    for table in doc.tables:
        for r_count, row in enumerate(table.rows):
            for c_count, cell in enumerate(row.cells):
                if r_count == 1 and c_count == 0:
                    for para in cell.paragraphs:
                        for run in para.runs:
                            print(f"Row = {r_count}, Col = {c_count}")
                            for ele in run._element:
                                print(f"  Child Tag: {ele.tag}")
                                for child in ele:
                                    print(f"    Grandchild Tag: {child.tag}")

#trans_case2()

from lxml import etree
 # Assuming doc is a loaded docx.Document object

# --- TARGET CELL ---
target_r = 1
target_c = 0
target_cell = doc.tables[0].rows[target_r].cells[target_c] 
tagget_cell1 = doc.tables[0].rows[4].cells[target_c]
global eq_count
eq_count = 0

def is_equation(p_element):
    M_NAMESPACE = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
    oMath_elements = p_element.findall(f'.//{M_NAMESPACE}oMath')
    
    if oMath_elements:
        return True
    else:
        return False
# --- ITERATE PARAGRAPHS IN THE CELL ---
def get_eq_info():
    for para in target_cell.paragraphs:
        # Access the paragraph's root XML element
        p_element = para._element 
        if is_equation(p_element):
            eq_count += 1
        print(f"\n--- FULL XML for Paragraph in R{target_r}, C{target_c} ---")
        
    for para in tagget_cell1.paragraphs:
        p_element = para._element 
        if is_equation(p_element):
            eq_count += 1
        print(f"\n--- FULL XML for Paragraph in R{target_r}, C{target_c} ---")


#print(eq_count)

#doc.save(save_path)


from lxml import etree 

# Define the Math XML namespace
M_NAMESPACE = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'

def extract_omath_xml(paragraph):
    """Searches a paragraph for OMath elements and returns the first one found."""
    p_element = paragraph._element
    omath_elements = p_element.findall(f'.//{M_NAMESPACE}oMath')
    return omath_elements[0] if omath_elements else None

def get_simple_omath_text(omath_element):
    """
    Method C: Recursively extracts all text content from an OMath XML element.
    WARNING: This loses all mathematical structure (e.g., x^2 will appear as x2).
    """
    if omath_element is None:
        return ""
        
    text_parts = []
    
    # The 'itertext()' method is the simplest way to get all text nodes in the element's subtree
    for text in omath_element.itertext():
        text_parts.append(text)
        
    # Join all the extracted text fragments into one string
    return "".join(text_parts).strip()

# --- Example Usage in your Table Loop ---

# Assuming 'doc' is your loaded document object
for table in doc.tables:
    for r_count, row in enumerate(table.rows):
        for c_count, cell in enumerate(row.cells):
            for para in cell.paragraphs:
                
                omath_element = extract_omath_xml(para)
                
                if omath_element is not None:
                    raw_equation_text = get_simple_omath_text(omath_element)
                    
                    print(f"[{r_count}, {c_count}] Found OMath. Raw Text: '{raw_equation_text}'")
                    
                # Continue with your image/text processing logic here...



    



