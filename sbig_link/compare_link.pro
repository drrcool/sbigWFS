readcol, 'SBIG_reference.dat', x1, y1
readcol, 'manual_wfs_0081.dao', x2, y2
readcol, 'link', ind1, ind2

readcol, 'f9newsys.cntr', x1, y1
readcol, 'auto_wfs_0005.dao', x2, y2
readcol, 'f9link', ind1, ind2

ind1 = ind1 -1
ind2 = ind2 -1

plot, x1, y1, ps=2
djs_oplot, x2, y2, ps=4, color='red'

for ii = 0, n_elements(ind1) -1 do begin
	
	djs_oplot, [x1[ind1[ii]],x2[ind2[ii]]], $
		[y1[ind1[ii]],y2[ind2[ii]]], color='green'
endfor




END

