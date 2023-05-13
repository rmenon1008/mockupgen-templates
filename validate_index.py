import json
import jsonschema
import os

def is_valid_image(path):
    """ Check if a file is a valid image. """
    if not os.path.isfile(os.path.join(os.path.dirname(__file__), path)):
        print(f"Image file not found: {path}")
        return False
    
    if not path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
        print(f"Invalid image file extension: {path}")
        return False
    
    return True

def validate_template(template):
    """ Validate a template object. """

    def print_error(msg):
        if 'slug' in template:
            print(f"Error validating template {template['slug']}")
        print(msg)

    # Ensure the required fields are present
    required_fields = ['slug', 'name', 'base_file', 'screen_points']
    for field in required_fields:
        if field not in template:
            print_error(f"Missing required field: {field}")
            return False
        
    # Ensure the base file exists
    if not is_valid_image(template['base_file']):
        return False
    
    # Ensure the screen points are valid
    if len(template['screen_points']) != 4:
        print_error("Screen points must have 4 points")
        return False
    for point in template['screen_points']:
        if len(point) != 2:
            print_error("Screen points must be 2D")
            return False
        
    # Ensure either mask_aspect_ratio or mask_file is valid
    if 'mask_aspect_ratio' in template and 'mask_file' in template:
        print_error("Template must have either mask_aspect_ratio or mask_file, not both")
        return False
    
    if 'mask_aspect_ratio' in template:
        if not isinstance(template['mask_aspect_ratio'], float):
            print_error("Mask aspect ratio must be a float")
            return False
    elif 'mask_file' in template:
        if not is_valid_image(template['mask_file']):
            return False
    else:
        print_error("Template must have either mask_aspect_ratio or mask_file")
        return False
    
    # Ensure categories are valid
    if 'categories' in template:
        if not isinstance(template['categories'], list):
            print_error("Categories must be a list")
            return False
        for category in template['categories']:
            if not isinstance(category, str):
                print_error("Categories must be strings")
                return False
            
    # Ensure the author is valid
    if 'author' in template:
        if not isinstance(template['author'], str):
            print_error("Author must be a string")
            return False
        
    # Ensure the backlink is valid
    if 'backlink' in template:
        if not isinstance(template['backlink'], str):
            print_error("Backlink must be a string")
            return False
    
    # Ensure brightness and contrast are valid
    if 'brightness' in template:
        if not isinstance(template['brightness'], float):
            print_error("Brightness must be a float")
            return False
    if 'contrast' in template:
        if not isinstance(template['contrast'], float):
            print_error("Contrast must be a float")
            return False
        
    # Ensure there are no extra fields
    all_fields = required_fields + ['mask_aspect_ratio', 'mask_file', 'brightness', 'contrast', 'categories', 'author', 'backlink']
    for field in template:
        if field not in all_fields:
            print_error(f"Unexpected field: {field}")
            return False
        
    return True



INDEX_PATH = os.path.join(os.path.dirname(__file__), 'index.json')

if __name__ == "__main__":
    # Load the index
    try:
        with open(INDEX_PATH) as index_file:
            index = json.load(index_file)
    except FileNotFoundError:
        print("Index file not found")
        exit(1)

    if "templates" not in index:
        print("Index missing templates")
        exit(1)
    
    # Validate the index
    for i, template in enumerate(index["templates"]):
        if not validate_template(template):
            exit(1)
    
    print("Index validated successfully")