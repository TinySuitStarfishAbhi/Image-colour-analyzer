try:
	import streamlit as st
	import os
	import cv2
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib import colors
	from collections import Counter
	from sklearn.cluster import KMeans
	from io import BytesIO, StringIO
	print("All modules loaded successfully!")
except Exception as e:
	print("Something is amiss: {}".format(e))

STYLE = """
<style>
img {
	max-width: 100%
}
</style>
"""

def rgb_to_hex(rgb_colour):
    hex_colour = "#"
    for i in rgb_colour:
        hex_colour += ("{:02x}".format(int(i)))
    return hex_colour

st.title("Image Colour Analyzer")
st.markdown("**An application that detects colours of any image and calculates their weights!**")
st.write("Upload any image of the type: JPG, JPEG or PNG")
st.write("Give it a few seconds, then scroll down :D ")
st.write("The number of colours is set to 5 as default, you can change it as well.")

st.markdown(STYLE, unsafe_allow_html = True)
image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if image is not None:
	img_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
	opencv_image = cv2.imdecode(img_bytes, 1)
	st.image(opencv_image, channels="BGR")
	n = st.number_input('Colours', min_value=1, max_value=10, value=5, step=1)
	opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
	modified_img = cv2.resize(opencv_image, (900, 600), interpolation = cv2.INTER_AREA)
	modified_img = modified_img.reshape(modified_img.shape[0]*modified_img.shape[1], 3)
	clf = KMeans(n_clusters = n)
	colour_labels = clf.fit_predict(modified_img)
	center_colours = clf.cluster_centers_
	counts = Counter(colour_labels)
	ordered_colours = [center_colours[i] for i in counts.keys()]
	hex_colours = [rgb_to_hex(ordered_colours[i]) for i in counts.keys()]
	st.set_option('deprecation.showPyplotGlobalUse', False)
	plt.figure(figsize = (12, 8))
	plt.pie(counts.values(), labels = hex_colours, colors = hex_colours)
	st.write(hex_colours)
	st.pyplot()
