%%%%%%% R-Clustering demo file
% This demo applies the R-Clustering segmentation algorithm on a set
% captured by a lifelogging wearable camera.
%
% For a visualization of the result, use the 'plot_params' variable in 
% loadParametersDemo.m.

% Load parameters
loadParametersDemo;

% Folder with lifelogging images that we want to segment
%folder = [pwd '/test_data/Subject1'];'/media/HDD_2TB/DATASETS/LIFELOG_DATASETS/Narrative/imageSets/Berta/27_Crop_informative_images'
folders = {'/media/HDD_2TB/DATASETS/LIFELOG_DATASETS/Narrative/imageSets/Berta/26_Crop_informative_images'};

for i=1:length(folders)
    folder = folders{i};
    % Format of the images in 'folder
    images_format = '.jpg';


% .csv, .txt or .xls file with the GT segmentation of the data
% (OPTIONAL, set to empty string if you don't want an evaluation of the result) 
% GT_path = [pwd '/test_data/GT/GT_Subject1.csv'];
    GT_path ='';

    %% The R-Clustering segmentation is applied
    segmentation = RClustering(folder, images_format, data_params, R_Clustering_params, CNN_params, Semantic_params, plot_params, GT_path);
end
    disp('Done');
    exit
