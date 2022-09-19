# UTILITIES
import os, io

def read_files(dir, ftype="txt"):
    import fitz

    prev_dir = os.getcwd()
    print(f"changing cwd to {dir}")
    os.chdir(dir) 
    print(f"reading files...")
    file_list = [ file_name for file_name in os.listdir(dir) 
                    if file_name[-len(ftype):] == ftype ]
    for file_name in file_list:
        #TODO : remove slicing after devel
        print(f"reading {file_name}")
        yield fitz.open(os.path.join(file_name))
    os.chdir(prev_dir)

def read_images_from_pdf(files, out_dir):
    from PIL import Image

    for pdf in files:
        file_name = os.path.splitext(pdf.name)[0]
        images = sum([ pdf[i].get_images() for i in range(len(pdf)) ], [])
        print(f"{len(images)} images in file : {file_name}")

        page_out_dir = os.path.join(out_dir, file_name)
        os.makedirs(page_out_dir)
        for n, image in enumerate(images):
            xref = image[0]
            
            extract = pdf.extract_image(xref)
            image = Image.open(io.BytesIO(extract["image"]))
            image.save(open(f"{page_out_dir}/img_{n}.{extract['ext']}", "wb"))

def read_text_from_pdf(files, out_dir):
    for pdf in files:

        file_name = os.path.splitext(pdf.name)[0]
        out_file = os.path.join(out_dir, file_name)
        text = str()

        for page in pdf: text += page.getText()
        print(text)

        with open(f"{out_file}.txt", "w") as f:
            f.write(text)


if __name__=="__main__":
    pdf_dir = os.path.join(os.getcwd(), "pdf")
    out_dir = os.path.join(os.getcwd(), "out")
    files = [ pdf for pdf in read_files(dir=pdf_dir, ftype="pdf") ]
    read_images_from_pdf(files, out_dir)

    