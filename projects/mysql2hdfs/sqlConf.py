#!/usr/bin/env python
#coding:utf-8
'''
sqls statement
'''

# saled ticket
sql1 = """SELECT t1.cinema_sell_id
,t1.cinema_movie_show_id
,CONCAT(t1.cinema_ticket_flag_1,"_",t1.cinema_ticket_flag_2) orderid
,'' areanum
,t1.cinema_seat_info
,t1.cinema_ticket_type
,t1.cinema_ticket_income
,'' cinema_sell_channel
,'' tax
,'' ticket_price
,'' ticket_tax
,0 is_refund
,IF(t1.cinema_book_id>0,1,0) is_book
,t1.cinema_user_id
,'' last_user_id
,'' tax_name
,t1.cinema_book_fee
,'' book_fee_tax
,'' book_fee_tax_name
,'' book_fee_tag
,'' cinema_refund_channel 
,t1.cinema_service_charge_name
,t1.cinema_service_charge_value
,'' checkcounts 
,t1.cinema_vip_id
,IF(LENGTH(t1.cinema_membercard_id)>2,1,0) is_member
,IF(cinema_person_num>1,1,0) is_mergon
,t1.cinema_ticket_qrcode
,t1.cinema_sell_time
,'' cinema_refund_time
,'' cinema_update_time
,'' posorderid
,0 is_add
,t1.cinema_sell_fee
,t1.work_station_group_id
,t1.work_station_id
,t1.cinema_ticket_report_type
FROM cinema_sell_log t1 
WHERE t1.cinema_sell_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s')
and t1.cinema_sell_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')"""

# ticket refunded
sql2 = """SELECT t1.cinema_sell_id
,t1.cinema_movie_show_id
,CONCAT(t1.cinema_ticket_flag_1,"_",t1.cinema_ticket_flag_2) orderid
,'' areanum
,t1.cinema_seat_info
,t1.cinema_ticket_type
,-1*t1.cinema_ticket_income cinema_ticket_income
,'' cinema_sell_channel
,'' tax
,'' ticket_price
,'' ticket_tax
,1 is_refund
,IF(t1.cinema_book_id>0,1,0) is_book
,t1.cinema_user_id
,'' last_user_id
,'' tax_name
,t1.cinema_book_fee
,'' book_fee_tax
,'' book_fee_tax_name
,'' book_fee_tag
,t2.cinema_refund_channel 
,t1.cinema_service_charge_name
,t1.cinema_service_charge_value
,'' checkcounts 
,t1.cinema_vip_id
,IF(LENGTH(t1.cinema_membercard_id)>2,1,0) is_member
,IF(t1.cinema_person_num>1,1,0) is_mergon
,t1.cinema_ticket_qrcode
,t1.cinema_sell_time cinema_sell_time
,t2.cinema_refund_time cinema_refund_time
,'' cinema_update_time
,'' posorderid
,0 is_add
,t1.cinema_sell_fee
,t1.work_station_group_id
,t1.work_station_id
,t1.cinema_ticket_report_type
FROM cinema_sell_log t1 , cinema_refund_log t2 
WHERE t1.cinema_sell_id=t2.cinema_sell_id 
and t2.cinema_refund_time  >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s')
and t2.cinema_refund_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')"""

# ticket register again
sql3 = """SELECT t1.cinema_sell_add_id cinema_sell_id
,t1.cinema_sell_add_showid cinema_movie_show_id
,t1.cinema_sell_add_id orderid
,'' areanum
,t2.seat_info cinema_seat_info
,t1.cinema_sell_add_desc cinema_ticket_type
,t2.ticket_income cinema_ticket_income
,'' cinema_sell_channel
,'' tax
,'' ticket_price
,'' ticket_tax
,0 is_refund
,0 is_book
,t1.cinema_create_uid cinema_user_id
,t1.cinema_update_uid last_user_id
,'' tax_name
,'' cinema_book_fee
,'' book_fee_tax
,'' book_fee_tax_name
,'' book_fee_tag
,'' cinema_refund_channel 
,'' cinema_service_charge_name
,'' cinema_service_charge_value
,'' checkcounts 
,'' cinema_vip_id
,0 is_member
,0 is_mergon
,'' cinema_ticket_qrcode
,t1.cinema_create_time cinema_sell_time
,'' cinema_refund_time
,t1.cinema_update_time cinema_update_time
,'' posorderid
,1 is_add
,'' cinema_sell_fee
,'' work_station_group_id
,'' work_station_id
,'' cinema_ticket_report_type
FROM cinema_sell_add t1 LEFT JOIN cinema_sell_add_detail t2 ON t1.cinema_sell_add_id=t2.cinema_sell_add_id
LEFT JOIN cinema_movie_show t3 ON t1.cinema_sell_add_showid=t3.cinema_movie_show_id
WHERE ((TYPE=1 AND cinema_sell_add_status=1) OR (TYPE=2 AND zz_audit_status=1))
  AND t1.cinema_create_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s')
  AND t1.cinema_create_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')"""

# pay info
sql4 = """SELECT cinema_sell_id,orderid,paytype,paytypename,payval ,1 nums,cinema_check_num,
 cinema_bankcard_id,
 cinema_membercard_id,
 cinema_quan_id,is_cash,vipcardtype,is_add,cinema_sell_time cinema_pay_time FROM(
SELECT cinema_sell_id
,CONCAT(t1.cinema_ticket_flag_1,"_",t1.cinema_ticket_flag_2) orderid,
CASE t2.id WHEN 1 THEN 'cash' WHEN 2 THEN 'bankcard' WHEN 3 THEN 'duihuanquan' WHEN 4 THEN 'membercard' WHEN 5 THEN 'check' WHEN 6 THEN 'zhaodai' WHEN 7 THEN 'xianjinquan' WHEN 8 THEN 'zongbuquan' WHEN 9 THEN 'yushouquan' WHEN 10 THEN 'jifen' END paytype,
CASE t2.id WHEN 1 THEN '现金' WHEN 2 THEN '银行卡' WHEN 3 THEN '兑换券' WHEN 4 THEN '会员卡' WHEN 5 THEN '支票' WHEN 6 
THEN '招待' WHEN 7 THEN '现金券' WHEN 8 THEN '总部券' WHEN 9 THEN '预售券' WHEN 10 THEN '积分兑换' END paytypename,
CASE WHEN t2.id = 1 THEN t1.cinema_pay_money
     WHEN t2.id = 2 THEN t1.cinema_bank_value
     WHEN t2.id = 3 AND LENGTH(t1.cinema_exchange_count)>0 AND t1.cinema_exchange_value>0 THEN t1.cinema_exchange_value
     WHEN t2.id = 3 AND LENGTH(t1.cinema_exchange_count)>0 AND t1.cinema_exchange_value=0 THEN t1.cinema_ticket_income         
     WHEN t2.id = 4 THEN t1.cinema_membercard_value
     WHEN t2.id = 5 THEN t1.cinema_check_value
     WHEN t2.id = 6 THEN t1.cinema_zhaodai_value
     WHEN t2.id = 7 THEN t1.cinema_xianjinquan_value
     WHEN t2.id = 8 THEN t1.cinema_zongbuquan_value
     WHEN t2.id = 9 AND LENGTH(t1.cinema_yushouquan_count)>0 AND t1.cinema_yushouquan_value>0 THEN t1.cinema_yushouquan_value
     WHEN t2.id = 9 AND LENGTH(t1.cinema_yushouquan_count)>0 AND t1.cinema_yushouquan_value=0 THEN t1.cinema_ticket_income
     WHEN t2.id = 10 AND ratio_exchange_type=1 THEN t1.ratio_exchange_substitute_value
 END payval,
 cinema_check_num,
 cinema_bankcard_id,
 cinema_membercard_id,
 cinema_quan_id,
 IF(t1.cinema_pay_money>0,1,0) is_cash,
 '' vipcardtype,
 0 is_add,
 cinema_sell_time
FROM cinema_sell_log t1,
(SELECT 1 id UNION ALL
SELECT 2 id  UNION ALL
SELECT 3 id  UNION ALL
SELECT 4 id  UNION ALL
SELECT 5 id  UNION ALL
SELECT 6 id  UNION ALL
SELECT 7 id  UNION ALL
SELECT 8 id  UNION ALL
SELECT 9 id  UNION ALL
SELECT 10 id  ) t2
WHERE cinema_sell_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s') AND  cinema_sell_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')
) t3
WHERE payval >0 AND payval IS NOT NULL  
UNION ALL
SELECT t2.pay_business_id cinema_sell_id,CONCAT(t3.cinema_ticket_flag_1,"_",t3.cinema_ticket_flag_2) orderid,t2.pay_detail_name paytype,t1.cinema_pay_type_desc paytypename,t2.pay_detail_value payval ,1 nums
, '' cinema_check_num,
 '' cinema_bankcard_id,
 '' cinema_membercard_id,
 '' cinema_quan_id,
 ''  is_cash,
 '' vipcardtype,
 0 is_add,
 cinema_add_time cinema_pay_time
FROM cinema_pay_detail_vertical t2 LEFT JOIN cinema_pay_type t1 ON t1.cinema_pay_type_name = t2.pay_detail_name
LEFT JOIN cinema_sell_log t3 ON t2.pay_business_id=t3.cinema_sell_id
WHERE t2.pay_business_type=1 AND cinema_add_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s') AND  cinema_add_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')
UNION ALL
SELECT cinema_sell_add_id,cinema_sell_add_id orderid,cinema_sell_add_pay_type paytype,
CASE cinema_sell_add_pay_type WHEN 'cash' THEN '现金' WHEN 'check' THEN '支票' WHEN 'quan' THEN '券' ELSE '待补充' END  paytypename,
cinema_sell_add_total payval ,cinema_sell_add_num nums,'' cinema_check_num,
 '' cinema_bankcard_id,
 '' cinema_membercard_id,
 cinema_sell_add_quan_id cinema_quan_id,IF(cinema_sell_add_pay_type='cash',1,0) is_cash,'' vipcardtype,1 is_add, cinema_create_time cinema_pay_time
 FROM cinema_sell_add
 WHERE cinema_create_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s')
  AND cinema_create_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')"""

# ticket order
sql5 = """SELECT 
CONCAT(t1.cinema_ticket_flag_1,"_",t1.cinema_ticket_flag_2) orderid
,CASE WHEN t1.cinema_movie_show_start_time BETWEEN CONCAT(LEFT(t1.cinema_movie_show_start_time,10),' 00:00:00') AND CONCAT(LEFT(t1.cinema_movie_show_start_time,10),' 05:59:59') THEN DATE_ADD(LEFT(t1.cinema_movie_show_start_time,10), INTERVAL - 1 DAY) ELSE LEFT(t1.cinema_movie_show_start_time,10) END business_date 
,LEFT(t1.cinema_movie_show_start_time,10) orderdate
,COUNT(*) seats
,SUM(t1.cinema_ticket_income) cinema_ticket_income
,SUM(t1.cinema_ticket_income) cinema_pay_income
,t1.cinema_hall_id
,t1.cinema_movie_num
,t1.cinema_movie_show_start_date
,t1.cinema_movie_show_start_time
,'' areanum
,t1.cinema_movie_show_id
,COUNT(t3.cinema_refund_id) refund_nums
,t1.cinema_ticket_status
,t1.cinema_user_id
,t1.cinema_sell_time
,SUM(IFNULL(t1.cinema_sell_fee,0)+IFNULL(t1.cinema_book_fee,0)) fee
,t1.work_station_id
,t1.cinema_print_from m
,SUM(t1.cinema_service_charge_value) service_fee
,0 is_merge
,t1.cinema_membercard_id
,t2.cinema_card_phone
,t1.cinema_movie_id
,t1.cinema_sell_channel
,0 is_add
FROM cinema_sell_log t1 
LEFT JOIN cinema_card_info t2 ON t1.cinema_membercard_id=t2.cinema_card_num
LEFT JOIN cinema_refund_log t3 ON t1.cinema_sell_id=t3.cinema_sell_id
WHERE t1.cinema_person_num=1
and t1.cinema_sell_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s')
and t1.cinema_sell_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')
GROUP BY orderid
UNION ALL 

SELECT 
CONCAT(t1.cinema_ticket_flag_1,"_",t1.cinema_ticket_flag_2) orderid
,CASE WHEN t1.cinema_movie_show_start_time BETWEEN CONCAT(LEFT(t1.cinema_movie_show_start_time,10),' 00:00:00') AND CONCAT(LEFT(t1.cinema_movie_show_start_time,10),' 05:59:59') THEN DATE_ADD(LEFT(t1.cinema_movie_show_start_time,10), INTERVAL - 1 DAY) ELSE LEFT(t1.cinema_movie_show_start_time,10) END business_date 
,LEFT(t1.cinema_movie_show_start_time,10) orderdate
,COUNT(*) seats
,SUM(t1.cinema_ticket_income) cinema_ticket_income
,SUM(t1.cinema_ticket_income) cinema_pay_income
,t1.cinema_hall_id
,t1.cinema_movie_num
,t1.cinema_movie_show_start_date
,t1.cinema_movie_show_start_time
,'' areanum
,t1.cinema_movie_show_id
,COUNT(t3.cinema_refund_id) refund_nums
,t1.cinema_ticket_status
,t1.cinema_user_id
,t1.cinema_sell_time
,SUM(IFNULL(t1.cinema_sell_fee,0)+IFNULL(t1.cinema_book_fee,0)) fee
,t1.work_station_id
,t1.cinema_print_from
,SUM(t1.cinema_service_charge_value) service_fee
,1 is_merge
,t1.cinema_membercard_id
,t2.cinema_card_phone
,t1.cinema_movie_id
,t1.cinema_sell_channel
,0 is_add
FROM cinema_lianchang_sell_log t1
LEFT JOIN cinema_card_info t2 ON t1.cinema_membercard_id=t2.cinema_card_num
LEFT JOIN cinema_refund_log t3 ON t1.cinema_sell_id=t3.cinema_sell_id
where t1.cinema_sell_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s')
and t1.cinema_sell_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')
GROUP BY orderid

UNION ALL  
SELECT 
t1.cinema_sell_add_id orderid
,CASE WHEN t3.cinema_movie_show_start_time BETWEEN CONCAT(LEFT(t3.cinema_movie_show_start_time,10),' 00:00:00') AND CONCAT(LEFT(t3.cinema_movie_show_start_time,10),' 05:59:59') THEN DATE_ADD(LEFT(t3.cinema_movie_show_start_time,10), INTERVAL - 1 DAY) ELSE LEFT(t3.cinema_movie_show_start_time,10) END business_date 
,LEFT(t3.cinema_movie_show_start_time,10) orderdate
,cinema_sell_add_num seats
,t1.cinema_sell_add_total cinema_ticket_income
,t1.cinema_sell_add_total cinema_pay_income
,t3.cinema_hall_id
,t3.cinema_movie_num
,t3.cinema_movie_show_start_date
,t3.cinema_movie_show_start_time
,'' areanum
,cinema_movie_show_id
,0 refund_nums
,1 cinema_ticket_status
,t1.cinema_create_uid cinema_user_id
,t1.cinema_create_time cinema_sell_time
,0 fee
,'' work_station_id
,'' cinema_print_from
,0 service_fee
,0 is_merge
,'' cinema_membercard_id
,'' cinema_card_phone
,t3.cinema_movie_id
,'' cinema_sell_channel
,1 is_add
FROM cinema_sell_add t1 
LEFT JOIN cinema_movie_show t3 ON t1.cinema_sell_add_showid=t3.cinema_movie_show_id
WHERE t1.cinema_create_time >=  STR_TO_DATE('startTime','%Y-%m-%d %H:%i:%s')
  AND t1.cinema_create_time <  STR_TO_DATE('endTime','%Y-%m-%d %H:%i:%s')
GROUP BY orderid"""
