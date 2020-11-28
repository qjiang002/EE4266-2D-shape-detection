function newImg=img_preprocessing(Img)
%Turn the image into gray image
if size(Img,3) == 3
    Img=rgb2gray(Img);
end
%binarize the gray image
bwimg=imbinarize(Img, 'adaptive','ForegroundPolarity','dark','Sensitivity',0.4);
sizex=size(bwimg);
%inverse the black and white
for i=1:sizex(1)
    for j=1:sizex(2)
        if bwimg(i,j)==1
            bwimg(i,j)=0;
        elseif bwimg(i,j)==0
            bwimg(i,j)=1;
        end
    end
end
% remove noise
bwimg = medfilt2(bwimg);
newImg=bwimg;
end