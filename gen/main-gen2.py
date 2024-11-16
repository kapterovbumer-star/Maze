from Generator import *
from MazeGenerator import *
from PdfBuilder import *
import json

themes = ["water"]
pdf_builder = PdfBuilder("book2/mazes.pdf")

print("Generating the mazes...")
output_files= []
for difficulty in range(1,11):
    for size in range(10, 40, 5):
        for theme in themes:
            mg = MazeGenerator(width=size, height=size, difficulty=difficulty)
            mg.generate()
            maze_data = mg.export()
            
            gen = Generator(grid=False, maze_data=maze_data, maze_settings='sprites/Grass.json')
            output_filename = gen.render(filename=f"book2/maze-{difficulty}-{theme}-{size}.png", theme=theme)
            output_files.append({
                "title": f"Difficulty: {difficulty} - Size: {size}x{size}",
                "image_filename": output_filename
            })
with open("book2/mazes.json", "w") as file:
    file.write(json.dumps(output_files))
print("Generating the PDF...")
pdf_builder.create_pdf(output_files)