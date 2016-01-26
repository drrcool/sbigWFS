file = "reference_1.fits"

im = readfits(file)
atv, im

find, im, x, y, flux, sharp, round, 10000, 35, [-1.0, 1.0], [0, 1.0]
atvplot, x, y, ps=1

mask = x*0+1
for ii = 0, n_elements(x) -1 do begin

   dist = sqrt((x[ii]-x)^2+(y[ii]-y)^2)
   
   k = where(dist lt 100, ct)
   if ct gt 1 then begin
      mask[k] = 0
      mask[k[0]] = 1
      x[k[0]] = djs_median(x[k])
      y[k[0]] = djs_median(y[k])
   endif
endfor


kk = where(mask eq 1)
atvplot, x[kk], y[kk], color='green', ps=2

openw, 1, "SBIG_reference.dat"
for ii = 0, n_elements(kk) -1 do begin
   printf, 1, string(x[kk[ii]], format="(f8.3)") + ' ' + string(y[kk[ii]], format='(f8.3)')
endfor
close, 1

centerx = djs_mean(x[kk])
centery = djs_mean(y[kk])
openw, 1, "SBIG_reference.center"
printf, 1, string(centerx) + ' ' + string(centery)
close, 1


END
