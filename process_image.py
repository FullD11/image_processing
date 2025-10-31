import cv2
import numpy as np
import json
import sys

def poly_to_latex(coeffs):
    terms = []
    degree = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        power = degree - i
        if abs(c) < 1e-10:
            continue
        if power == 0:
            terms.append(f"{c:.4f}")
        elif power == 1:
            terms.append(f"{c:.4f}*t")
        else:
            terms.append(f"{c:.4f}*t^{power}")
    return " + ".join(terms).replace("+ -", "- ")

def process_image(image_path):
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"ERROR: Cannot read image at {image_path}", file=sys.stderr)
        sys.exit(1)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_bg = np.array([0, 0, 200])
    upper_bg = np.array([180, 30, 255])
    mask = cv2.bitwise_not(cv2.inRange(hsv, lower_bg, upper_bg))
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_data = []
    
    for contour in contours:
        if len(contour) < 6:
            continue
            
        t = np.linspace(0, 1, len(contour))
        x_vals = contour[:, 0, 0]
        y_vals = contour[:, 0, 1]
        
        p_x = np.polyfit(t, x_vals, 5)
        p_y = np.polyfit(t, y_vals, 5)
        
        p_x_latex = poly_to_latex(p_x)
        p_y_latex = poly_to_latex(p_y)
        
        contours_data.append({
            'p_x': p_x.tolist(),
            'p_y': p_y.tolist(),
            'latex_x': p_x_latex,
            'latex_y': p_y_latex
        })
    
    return contours_data

if __name__ == "__main__":
    image_path = sys.argv[1]
    contours = process_image(image_path)
    print(json.dumps(contours))