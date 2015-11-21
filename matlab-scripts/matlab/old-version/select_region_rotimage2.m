function    rect_final = select_region_rotimage2(image_rot)

    im_gray=rgb2gray(image_rot);
    im_diag=diag(im_gray);

	corn_aux=find(im_diag>0);
    ini=corn_aux(1);
    fin=corn_aux(end);

    %-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    %Primer area
    ini_x=ini; ini_y=ini; fin_x=fin; fin_y=fin;
    
    %miramos maxima anchura (ini)
	fila1=find(im_gray(ini_x,:)>0);
    p2_y=fila1(end);
        if p2_y<fin_y
            fin_y=p2_y;
        end
    %miramos maxima anchura (fin)
	fila2=find(im_gray(fin,:)>0);
    p4_y=fila1(1);
        if p4_y>ini_y
            ini_y=p4_y;
        end
        
    %miramos maxima altura (ini)
    col1=find(im_gray(:,ini_y)>0); 
    p4_x=col1(end);
        if p4_x<fin_x
            fin_x=p4_x;
        end
    %miramos maxima altura (fin)   
    col2=find(im_gray(:,fin_y)>0); 
    p2_x=col1(1);
        if p2_x>ini_x
            ini_x=p2_x;
        end

    
          
    xmin1=ini_y; ymin1=ini_x;
    width1=abs(fin_y-ini_y);height1=abs(fin_x-ini_x); 
    
    rect1=[xmin1 ymin1 width1 height1];
    rect_final=rect1;    
    %im_Crop1=imcrop(image_rot, rect1);
    %figure,imshow(im_Crop1)     
            
end



