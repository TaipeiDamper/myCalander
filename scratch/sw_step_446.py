Created At: 2026-05-22T03:56:09Z
Completed At: 2026-05-22T03:56:09Z
File Path: `file:///c:/Users/ASAHI/Desktop/Personal_Research/dylan_otherCode/calander/stock/stock_widget.py`
Total Lines: 721
Total Bytes: 34417
Showing lines 461 to 485
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
461:                     if key in ["ma20", "low20", "nav"]:
462:                         h_offset = 3
463:                         color = StockStyle.PRIMARY_GREY
464:                     else:
465:                         h_offset = 4
466:                         # ETF 買點退化時，將強烈買進與買進價位顏色淡化
467:                         if is_degraded and key in ["strongBuyPrice", "buyPrice"]:
468:                             color = "#e0e0e0"
469:                         else:
470:                             color = StockStyle.PRIMARY_GREY
471:                     
472:                     canvas.create_line(xk, y1 - h_offset, xk, y1 + h_offset, fill=color, width=1)
473:                     canvas.stock_coords.append({'x': xk, 'val': val, 'lbl': name})
474:             
475:             # E. 繪製現價指針 (空心三角形，依漲跌改方向，平盤為圓圈)
476:             if curr > prev:
477:                 # 向右空心三角形
478:                 points = [xc+4, y1, xc-3, y1-4, xc-3, y1+4]
479:                 canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
480:             elif curr < prev:
481:                 # 向左空心三角形
482:                 points = [xc-4, y1, xc+3, y1-4, xc+3, y1+4]
483:                 canvas.create_polygon(points, fill="#f0f0f0", outline=StockStyle.PRIMARY_GREY, width=1)
484:             else:
485:                 # 平盤圓圈
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
