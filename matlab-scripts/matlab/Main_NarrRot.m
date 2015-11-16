% Main Methods - Votation - Sliding Window - Visualization

clear all; close all

carpeta='17';
path_carpeta = '/Users/marccarneherrera/Pictures/Narrative Clip/marc.carne.herrera@gmail.com/clip_9521902d/2015/09';

% Images Directory
Folder_Images= ([path_carpeta '/' carpeta]);
files_images=dir(fullfile(Folder_Images));
    %Doc Metadata
    Folder_Meta= ([Folder_Images '/Meta']);
    files_meta=dir(fullfile(Folder_Meta));
    
    
% Rotated Images
Folder_Rot= ([path_carpeta '/' carpeta '_Rot']);   
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
                   
                %3) Based on the Narrative Metadata and using the communitie equation   
                angle=180*(atan2(0,-1)-atan2(data.acc_data.samples(1),data.acc_data.samples(2)))/atan2(0,-1); 
                angles(p,1)=angle-270;
                
                image_rot=imrotate(image,angles(p,1));%, 'bicubic');    
                cadena=strcat(Folder_Rot,'/',filename_aux,'.jpg');
                imwrite(image_rot,cadena,'jpg'); 
   
            end
        end
        