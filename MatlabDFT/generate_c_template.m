img=imread('origin_c.jpg');
%transform to gray image
if size(img,3) == 3
img=rgb2gray(img);
end
bwimg = img_processing(img)
%percentage of fourier descriptors used to recover image
usedPercent=0.3;

[rows, cols]=size(img);
figure('Name','original image','NumberTitle','off');
title1=sprintf('original image');
imshow(bwimg),title(title1);


Bd=findBoundary(bwimg,8,'cw');
Xwhole = [];
Ywhole = [];
for i = 1:size(Bd,1)
BdPoints=Bd{i};
X=BdPoints(:,1);
Y=BdPoints(:,2);
Xwhole = [Xwhole;X];
Ywhole = [Ywhole;Y];
end
noPts=length(Xwhole);
%%========================================================================%
%show original image in gray format
figure('Name','original image remove noise','NumberTitle','off');
title1=sprintf('remove noise original image,%d points',noPts);
imshow(bwimg),title(title1);

%%========================================================================%
%set true to save edge points(X,Y) to txt file
if 1
f=fopen('2_edge.txt','w');
for k=1:noPts
fprintf(f,'%d\t%d\n',Xwhole(k),Ywhole(k));
% dis_img(Xwhole(k),Ywhole(k))=255;
end
fclose(f);
end


%%========================================================================%
%set true to display 8-connectivity edge points extraction step by step
if 1
dis_img=zeros(rows,cols);
figure('Name','8-connectivity edge points extraction','NumberTitle','off');
for k=1:noPts
dis_img(Xwhole(k),Ywhole(k))=255;
% imshow(dis_img);
% pause(0.005);
end
imshow(dis_img),title('8-connectivity contour extraction');

end

%discrete fourier transform
%s->original edge points,must be of size n-by-2.
%z->complex numbers, coefficients of fourier transform.
s=[X Y];
z=frdescp(s);

%inverse fourier transform with part of fourier descriptors
%nr is total number of coefficients, within them, nb are used in recovery.
[nr,nc]=size(z);
nd=round(usedPercent*nr);

%s_recov -output of inverse fourier transform,coordinates of recovered edge
%points,n-by-2 format,n is same as original edge points number.
s_recov=ifrdescp(z,nd);
s_recov=uint16(s_recov);


%show recovered image
img1=zeros(rows,cols);
[rs, cs]=size(s_recov);
for k=1:rs
img1(s_recov(k,1),s_recov(k,2))=255;
end

%%show recovered image using part of fourier coefficients.
title2=sprintf('%d%% ( %d ) Fourier descriptors used',usedPercent*100,nd);
figure('Name','30%recovered image','NumberTitle','off');
imshow(img1),title(title2);



