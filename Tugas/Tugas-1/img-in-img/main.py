from PIL import Image


def int_to_bin(rgb):
    """merubah nilai bit rgb menjadi nilai biner"""
    r, g, b = rgb
    return ('{0:08b}'.format(r),
            '{0:08b}'.format(g),
            '{0:08b}'.format(b))


def bin_to_int(rgb):
    """ merubah nilai bit rgb kembali menjadi decimal"""
    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))


def merge_rgb(rgb1, rgb2):
    """menggabungkan nilai rgb 1 dengan nilai rgb 2"""
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    rgb = (r1[:4] + r2[:4],
           g1[:4] + g2[:4],
           b1[:4] + b2[:4])
    return rgb


def merge(img1, img2):
    """membuat gambar baru dari pergabungan nilai rgb yang di lakukan"""

    # cek gambar penampung harus lebih besar
    if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
        raise ValueError('gambar penampung harus lebih besar')

    pixel_map1 = img1.load()
    pixel_map2 = img2.load()

    new_image = Image.new(img1.mode, img1.size)
    pixels_new = new_image.load()

    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            rgb1 = int_to_bin(pixel_map1[i, j])

            rgb2 = int_to_bin((0, 0, 0))

            if i < img2.size[0] and j < img2.size[1]:
                rgb2 = int_to_bin(pixel_map2[i, j])

            rgb = merge_rgb(rgb1, rgb2)

            pixels_new[i, j] = bin_to_int(rgb)

    return new_image


def unmerge(img):
    pixel_map = img.load()

    new_image = Image.new(img.mode, img.size)
    pixels_new = new_image.load()

    original_size = img.size

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            
            r, g, b = int_to_bin(pixel_map[i, j])

            rgb = (r[4:] + '0000',
                   g[4:] + '0000',
                   b[4:] + '0000')

            pixels_new[i, j] = bin_to_int(rgb)

            if pixels_new[i, j] != (0, 0, 0):
                original_size = (i + 1, j + 1)

    new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

    return new_image


def merger(img1, img2, output):
    merged_image = merge(img1, img2)
    merged_image.save(output)


def unmerger(img, output):
    unmerged_image = unmerge(Image.open(img))
    unmerged_image.save(output)


pil = int(input("menu:\n 1. Gabungkan\n 2. Pisahkan\n pilih: "))
if pil == 1:
    img1_name = input("Gambar penampung : ")
    img2_name = input("gambar rahasia : ")
    print("proses...")
    img_1 = Image.open(img1_name)
    img_2 = Image.open(img2_name)
    if img_2.size < img_1.size:
        merger(img_1, img_2, 'output.png')
        print("'output.png' sukses dibuat")
    else:
        print("First image should be larger!")
elif pil == 2:
    img3 = input("masukan gambar: ")
    print("ekstraksi....")
    unmerger(img3, 'extracted.png')
    print("'extracted.png' adalah gambar rahasia")