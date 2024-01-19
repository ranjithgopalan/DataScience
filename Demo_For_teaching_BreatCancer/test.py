import os
file_path = "Data/cell_images/train"

try:
 for x in os.listdir(file_path):
   if 'other' in x:
      os.remove(os.path.join(file_path, x))
      print("File deleted successfully.")
     

    # delete the file
      
    
except OSError as error:
    print(f"Error: {error}")
    
    

 # We will run the same code for "parasitized" as well as "uninfected" folders within the "train" folder
# for folder_name in ['/parasitized/', '/uninfected/']:
    
    # Path of the folder
images_path = os.listdir(train_dir )

for i, image_name in enumerate(images_path):
    
    try:
    
        # Opening each image using the path of that image
        image = Image.open(train_dir + image_name)

            # Resizing each image to (64, 64)
        image = image.resize((SIZE, SIZE))

            # Converting images to arrays and appending that array to the empty list defined above
        train_images.append(np.array(image))            
        train_labels.append(1)
        
    except Exception:
      pass

# Converting lists to arrays
train_images = np.array(train_images)
train_labels = np.array(train_labels)   