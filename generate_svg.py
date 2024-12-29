import svgwrite
from cairosvg import svg2png
import os

def generate_svg_circles(num_svgs=100, radius=10, canvas_size=(500, 100)):
    """
    Generates a list of SVG strings with a circle moving horizontally across the canvas.
    
    Args:
        num_svgs (int): Number of SVG frames to generate.
        radius (int): Radius of the circle.
        canvas_size (tuple): Size of the SVG canvas as (width, height).
    
    Returns:
        list: List of SVG strings.
    """
    svgs = []
    for i in range(num_svgs):
        dwg = svgwrite.Drawing(size=canvas_size)
        x = (canvas_size[0] / num_svgs) * i + radius
        y = canvas_size[1] / 2
        dwg.add(dwg.circle(center=(x, y), r=radius, fill='blue'))
        svgs.append(dwg.tostring())
    return svgs

# Example usage
if __name__ == "__main__":
    svg_circles = generate_svg_circles()
    
    # Create output directory for PNGs
    output_dir = 'png_frames'
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, svg in enumerate(svg_circles):
        png_filename = os.path.join(output_dir, f'circle_{idx}.png')
        try:
            # Convert SVG string to PNG and save
            svg2png(bytestring=svg.encode('utf-8'), write_to=png_filename)
            print(f'Converted {png_filename}')
        except Exception as e:
            print(f'Error converting circle_{idx}.svg to PNG: {e}')