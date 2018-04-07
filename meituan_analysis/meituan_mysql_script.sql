#sql1
select distinct 
b.poi_id,b.title,b.avg_price,b.avg_score,b.comment_num,b.address,b.stamp from meituan_classify_info as a
inner join meituan_shop_info as b on a.sub_id = b.sub_id and a.class_type = b.class_type
where a.class_type = 1 and a.sub_id not in(24,393,395) and b.avg_price <> 0 and b.avg_score <> 0
order by avg_price desc;

#sql2
select distinct sub_id,sub_name from meituan_classify_info
where class_type = 1 and sub_id not in(24,393,395);

select distinct poi_id,avg_price from meituan_shop_info
where sub_id = 35 and class_type = 1;
    
-- sql3
select distinct a.sub_id,a.sub_name,
b.poi_id,b.title,b.avg_price,b.avg_score,b.comment_num,b.address from meituan_classify_info as a
inner join meituan_shop_info as b on a.sub_id = b.sub_id and a.class_type = b.class_type
where a.class_type = 1 and a.sub_id not in(24,393,395) and b.avg_price <> 0 and b.avg_score <> 0 
and CONCAT(b.sub_id,b.poi_id) not in ('6342030772','4050576755','6350576755','4052163162','2006068147006','5452800270','4087812358','6387812358','543311762')
order by b.comment_num desc limit 10;

-- sql4
select sub_id,sub_name ,count(*) as cnt from (
	select distinct a.sub_id,a.sub_name,
	b.poi_id,b.title,b.avg_price,b.avg_score,b.comment_num,b.address,b.stamp from meituan_classify_info as a
	inner join meituan_shop_info as b on a.sub_id = b.sub_id and a.class_type = b.class_type
	where a.class_type = 1 and a.sub_id in (55,56,57,58,59,60,62,227,233,20003,20059,20060)
    and b.avg_price <> 0 and b.avg_score <> 0 
) as x
group by sub_id,sub_name;

-- sql4
select distinct a.sub_id,a.sub_name,
b.poi_id,b.title,b.avg_price,b.avg_score,b.comment_num,b.address,b.stamp from meituan_classify_info as a
inner join meituan_shop_info as b on a.sub_id = b.sub_id and a.class_type = b.class_type
where a.class_type = 1 and a.sub_id = 20059 and b.avg_price <> 0 and b.avg_score <> 0;