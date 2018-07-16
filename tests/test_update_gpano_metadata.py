from image_processing import update_gpano_metadata

filename = 'samples/xmp/pano-cityscape-270.jpg'
if update_gpano_metadata(filename, 270):
    print("Added GPano metadata successfully")
else:
    print("Failed to add GPano Metadata")
