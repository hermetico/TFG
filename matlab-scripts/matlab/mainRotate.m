
%% Parameters

if exist('folder', 'var'),
  path_folder=folder;
else
  path_folder='/home/hermetico/Pictures/test matlab/fotos/2/2015/03/20';
end

% check main folder
if(~exist(path_folder, 'file'))
    return;
end

    
% check meta folder
if(exist([path_folder '/Meta'], 'file'))
    folder_meta = [path_folder '/Meta'];
elseif(exist([path_folder '/meta'], 'file'))
    folder_meta = [path_folder '/meta'];
else
    return;
end

format = '.jpg';


%% Start processing
disp(['Processing ' path_folder]);

%% Resizing
if exist('output_size', 'var'),
  disp(['Resizing output to ' num2str(output_size) ' * ' num2str(output_size)]) 
end 


path_rot = [path_folder '_Crop'];
if(~exist([path_rot], 'dir'))
	mkdir(path_rot);
end


%% List images 
img_list = dir([path_folder '/*' format]);
img_list = img_list(arrayfun(@(x) x.name(1) ~= '.', img_list));
img_list = {img_list(:).name};
nImages = length(img_list);


processed_images=0;
%% Rotate and crop each image
for i = 1:nImages
	[~, im_name, ~] = fileparts(img_list{i});
	image_meta = [folder_meta '/' im_name '.json'];

	% Check if the corresponding meta file exists
	if(exist(image_meta, 'file'))
        % Reading .json info
        data=loadjson(image_meta);

        % Based on the Narrative Metadata and using the communitie equation   
        angle = 180*(pi-atan2(data.acc_data.samples(1),data.acc_data.samples(2)))/pi;
		angle = angle-270;

		% Read image, rotate, crop and store
		try
		    im = imread([path_folder '/' img_list{i}]);
		catch
		    warning(['Error reading image ' img_list{i}])
		    continue
		end

		im = imRotateCrop(im, angle);
        
        
        % im resize if output_size exists
        if exist('output_size', 'var'),
          %disp(['Resizing to ' num2str(output_size) ' * ' num2str(output_size)]) 
          im = imresize(im,[output_size output_size]);
        end    
        
        processed_images=processed_images+1;
		imwrite(im, [path_rot '/' img_list{i}]);
	end

	%% Show progress
	if(mod(i, 20) == 0 || i == nImages)
		disp(['Processed ' num2str(processed_images) '/' num2str(nImages) ' images.']);
	end
end
disp('Done');
disp(['Result stored in ' path_rot]);

%% exit condition
if exist('exit_on_end', 'var')
  exit();
end

