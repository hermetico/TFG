%Crop region of interest from rotated images

clear all; 
close all

carpeta='17';
path_carpeta = '/Users/marccarneherrera/Pictures/Narrative Clip/marc.carne.herrera@gmail.com/clip_9521902d/2015/09';

% Rotated Images
Folder_Rot= ([path_carpeta '/' carpeta '_Rot']);    
files_images=dir(fullfile(Folder_Rot));
% Masked Images
Folder_Crop= ([path_carpeta '/' carpeta '_Crop']);    
mkdir(Folder_Crop);
   
% Numero/Nombre de las imagenes con las que estamos trabajando
for i=1:(length(files_images)-4)% 4 por el meta
    filenumber=strread(files_images(i+4).name,'%s','delimiter','.');
    filename{i,1}=filenumber{1};
end

% Apply mask
p=0;
fin=length(files_images)-4;%doc-1 es meta
for i=1:(fin)
            p=p+1; % images angle rotation
            %Read image
            aux = strcat (Folder_Rot,'/',(files_images(i+4).name));
        	image_rot=imread (aux);
            
            filenumber=strread(files_images(i+4).name,'%s','delimiter','.');
            filename_aux=filenumber{1};
                        
                %Crop region of interest
                rect=select_region_rotimage2(image_rot);

                %rect=[xmin ymin width height]
                im_cropped = imcrop(image_rot, rect);
                                
                %figure,imshow(im_cropped)    
                cadena=strcat(Folder_Crop,'/',filename_aux,'.jpg');
                imwrite(im_cropped,cadena,'jpg'); 
end