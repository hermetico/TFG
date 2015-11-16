%This scriot has been created to offer an easy application for Narrative
%users that want to put his images in a correct way due to the wrong angle
%colocation of the camera

%clear all; close all


if exist('folder', 'var'),
  path_carpeta_img=folder;
else
  path_carpeta_img=uigetdir('/','Seleccione el directorio de las imagenes');  
end

% Images Directory
Folder_Images= ([path_carpeta_img]);
files_images=dir(fullfile(Folder_Images));
    %Doc Metadata
    Folder_Meta= ([Folder_Images '/meta']);
    files_meta=dir(fullfile(Folder_Meta));
    
    
% Rotated Images
Folder_Rot= ([path_carpeta_img '_Rot']);   
mkdir(Folder_Rot);
    
% Numero/Nombre de las imagenes con las que estamos trabajando
for i=1:(length(files_images)-4)% 4 por el meta
    filenumber=strread(files_images(i+3).name,'%s','delimiter','.');
    filename{i,1}=filenumber{1};
end

p=0;
fin=length(files_images)-4;%doc-1 es meta
for i=1:(fin)
            p=p+1; % images angle rotation
            %Read image
            aux = strcat (Folder_Images,'/',(files_images(i+3).name));
        	image=imread (aux);
            
            filenumber=strread(files_images(i+3).name,'%s','delimiter','.');
            filename_aux=filenumber{1};
        
            if (exist([Folder_Meta '/' filename_aux '.json'], 'file')==2)
                % Reading .json info  %name=[filename,'.json'];
                imagemeta=([Folder_Meta,'/',filename_aux,'.json']);
                data=loadjson(imagemeta);
                   
                %3) Based on the Narrative Metadata and using the community equation   
                angle=180*(atan2(0,-1)-atan2(data.acc_data.samples(1),data.acc_data.samples(2)))/atan2(0,-1); 
                angles(p,1)=angle-270;
                
                image_rot=imrotate(image,angles(p,1));%, 'bicubic');    
                cadena=strcat(Folder_Rot,'/',filename_aux,'.jpg');
                imwrite(image_rot,cadena,'jpg'); 
   
            end
end
        

% Rotated Images
Folder_Rot= ([path_carpeta_img '_Rot']);    
files_images=dir(fullfile(Folder_Rot));
% Masked Images
Folder_Crop= ([path_carpeta_img '_Crop']);    
mkdir(Folder_Crop);

   
% Numero/Nombre de las imagenes con las que estamos trabajando
for i=1:(length(files_images)-2)% 4 por el meta
    filenumber=strread(files_images(i+2).name,'%s','delimiter','.');
    filename{i,1}=filenumber{1};
end

% Apply mask
p=0;
fin=length(files_images)-2;%doc-1 es meta
for i=1:(fin)
            p=p+1; % images angle rotation
            %Read image
            aux = strcat (Folder_Rot,'/',(files_images(i+2).name));
        	image_rot=imread (aux);
            
            filenumber=strread(files_images(i+2).name,'%s','delimiter','.');
            filename_aux=filenumber{1};
                        
                %Crop region of interest
                rect=select_region_rotimage2(image_rot);

                %rect=[xmin ymin width height]
                im_cropped = imcrop(image_rot, rect);
                               
                % redimensionamos la imagen si hay parametro de entrada
                if exist('output_size', 'var'),
                  im_cropped = imresize(im_cropped,[ output_size output_size])

                end             
                
                %figure,imshow(im_cropped)    
                cadena=strcat(Folder_Crop,'/',filename_aux,'.jpg');
                imwrite(im_cropped,cadena,'jpg'); 
end

rmdir(Folder_Rot, 's');

if exist('exit_on_end', 'var'),
  exit();
end
