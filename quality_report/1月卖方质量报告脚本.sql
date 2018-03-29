--报告量分布情况
--154 ReportDB

--A股
--select count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
--where create_date between'2018-01-01 00:00:00.000' and '2018-01-30 00:00:00.000' and report_type_id<>'28'


select left(CONVERT(varchar(100), create_date, 112),6),count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
where  right(CONVERT(varchar(100), create_date, 12),4) between 0101 and 0130 and report_type_id<>'28'
and year(create_date) between 2013 and 2018
group by left(CONVERT(varchar(100), create_date, 112),6)
order by left(CONVERT(varchar(100), create_date, 112),6)

--H股
--select count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
--where create_date between'2017-11-01 00:00:00.000' and '2017-11-30 00:00:00.000' and report_type_id='28'


select left(CONVERT(varchar(100), create_date, 112),6),count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
where  right(CONVERT(varchar(100), create_date, 12),4) between 0101 and 0130 and report_type_id='28'
and year(create_date) between 2013 and 2018
group by left(CONVERT(varchar(100), create_date, 112),6)
order by left(CONVERT(varchar(100), create_date, 112),6)
--非个股
--select count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT
--where create_date between'2018-01-01 00:00:00.000' and '2018-01-31 00:00:00.000'


select left(CONVERT(varchar(100), create_date, 112),6),count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT
where  right(CONVERT(varchar(100), create_date, 12),4) between 0101 and 0131
and year(create_date) between 2013 and 2018
group by left(CONVERT(varchar(100), create_date, 112),6)
order by left(CONVERT(varchar(100), create_date, 112),6)


--行业报告所属行业的分布情况
--0.154
--为空的剔除
select top 10 industry,count(*) as cnt from [192.168.0.154].[reportdb].dbo.T_RPT_BROWSER a
join report_type b 
on a.report_type_id=b.reporttypeid
where b.reporttypeid in (15,16,17,18,19,20) and 
industry <> '' and
create_date between'2018-01-01 00:00:00.000' and '2018-01-31 00:00:00.000'
group by industry 
order by count(*) desc



--近6月行业上榜次数
select count(*) as top_cnt, industry from
(
	select * from 
	(
		select row_number()over(partition by date order by cnt desc) as rk,* from 
		(
			select left(CONVERT(varchar(100), create_date, 12),4) as date ,industry,count(*) as cnt from [192.168.0.154].[reportdb].dbo.T_RPT_BROWSER a
			join report_type b 
			on a.report_type_id=b.reporttypeid
			where b.reporttypeid in (15,16,17,18,19,20) and 
			industry <> '' and
			create_date between '2017-08-01' and '2018-01-31'
			group by industry ,left(CONVERT(varchar(100), create_date, 12),4)
		) as a
	) as b
	where rk <=10
	--and right(date,1) <> datepart(mm,getdate())
) as c
group by industry
order by count(*) desc

select left(CONVERT(varchar(100), DATEADD(MONTH,-1,GETDATE()), 112),6) +'31'

--业绩预告、快报处理及时性
--0.11  gogoal
--朝阳永续公告处理及时性（巨潮）
--服务器：192.168.0.11  数据库：gogoal
/****** Script for SelectTopNRows command from SSMS  ******/
--抓取时间
drop table #trsgg,#tmp1,#4

SELECT
[hkey],
lasttime
  into #trsgg
FROM [192.168.0.153].[TRS_Results_Express].[dbo].[urlcontent]
--快报原始 drop table #tmp1
select
'kuaibao'bs,
a.guid,
a.publish_date,
a.into_date entrytime,
h.hkey,
h.status
into #tmp1
from [192.168.0.154].[reportdb].dbo.Performance_express_in a
left outer join [192.168.0.154].[reportdb].dbo.T_Results_Express_Handle_Log h
on a.guid=h.fileguid
where a.into_date>='2018-01-01 00:00:00'
and a.into_date<='2018-01-31 23:59:59'
and a.source= 1
and h.status= 1
--预告原始
insert into #tmp1
select
'yugao'bs,
a.guid,
a.publish_date,
a.into_date entrytime,
h.hkey,
h.status
from [192.168.0.154].[reportdb].dbo.Performance_forecast_in a
left outer join [192.168.0.154].[reportdb].dbo.T_Results_Express_Handle_Log h
on a.guid=h.fileguid
where a.into_date>='2018-01-01 00:00:00'
and a.into_date<='2018-01-31 23:59:59'
and a.source= 1
and h.status= 1


--join
select
a.bs 报告类型,
a.guid,
a.publish_date 巨潮时间,
t.lasttime 抓取时间,
case when (datepart(hh,a.publish_date)!= 0 or datepart(mi,a.publish_date)!= 0 or datepart(ss,a.publish_date)!= 0)then a.publish_date
else t.lasttime end 最终时间,
a.entrytime 录入时间
into #4
from #tmp1 a
left outer join #trsgg t
on a.hkey=t.hkey



--------------非工作时间 ---------------------------------------------
select 报告类型,count(*) 非工作时间 from #4 
where 最终时间 is not null and 最终时间>='2018-01-01 00:00:00'
and (DATEPART(hh, 最终时间)  <= 9 or DATEPART(hh, 最终时间) >= 21  or datepart(dw,最终时间) in (1,7))
group by 报告类型

----------------工作时间---------------------------------------------
--工作时间 <= 30 mins
select 报告类型 ,count(*) '工作时间<=30' from #4 
where 最终时间 is not null and 最终时间>='2018-01-01 00:00:00'
and datediff(minute, 最终时间, 录入时间) <= 30
and (DATEPART(hh, 最终时间)  >  9 or DATEPART(hh, 最终时间) < 21)
and datepart(dw,最终时间) not in (1,7)
group by 报告类型

--工作时间 > 30 mins
select 报告类型,count(*) '工作时间>30' from #4 
where 最终时间 is not null and 最终时间>='2018-01-01 00:00:00'
and datediff(minute, 最终时间, 录入时间) > 30
and (DATEPART(hh, 最终时间)  >  9 or DATEPART(hh, 最终时间) < 21)
and datepart(dw,最终时间) not in (1,7)
group by 报告类型

--分布情况
select 报告类型 as rpt_type,'01-' + cast(DATEPART(dd, 最终时间) as varchar(10)) as date,count(*) as cnt ,cast(cast(max(datediff(minute, 最终时间, 录入时间)) as float)/60 as decimal(10,2)) as hours from #4 
where 最终时间 is not null and 最终时间>='2018-01-01 00:00:00'
and datediff(minute, 最终时间, 录入时间) > 30
and DATEPART(hh, 最终时间)  between 9 and 21
and datepart(dw,最终时间) not in (1,7)
group by 报告类型,cast(DATEPART(dd, 最终时间) as varchar(10)),DATEPART(dd, 最终时间)
order by 报告类型,DATEPART(dd, 最终时间)

--公告总量
select * from #4



select * , datediff(minute, 最终时间, 录入时间) /60.0 from #4 
where 最终时间 is not null and 最终时间>='2018-01-01 00:00:00'
and datediff(minute, 最终时间, 录入时间) > 30
and (DATEPART(hh, 最终时间)  >  9 and DATEPART(hh, 最终时间) < 21)
and datepart(dw,最终时间) not in (1,7)
order  by 最终时间 ,录入时间 desc



SELECT * FROM [192.168.0.154].[reportdb].dbo.Performance_express_in

select * from 
(
	select 'KUAIBAO' rpt_type,GUID,ENTRYDATE, into_date,UPDATEDATE from  [192.168.0.154].[reportdb].dbo.Performance_express_in
	where source = 1
	and status = 4
	and is_valid = 1 
	UNION
	select 'YUGAO' rpt_type, GUID,ENTRYDATE,into_date,UPDATEDATE from  [192.168.0.154].[reportdb].dbo.Performance_forecast_in
	where source = 1
	and status = 4
	and is_valid = 1 
) as a
where entrydate between '2018-01-01' and '2018-01-31'
and datediff(minute, entrydate, into_date) > 30
and (DATEPART(hh, into_date)  >  9 and DATEPART(hh, into_date) < 21)
and datepart(dw,into_date) not in (1,7)
order by entrydate desc


select * from [192.168.0.154].[reportdb].dbo.Performance_express_in

-----------------------------------------------------------------------------------

--超预期寻宝线索占比情况
--0.11
select count(*)
from[gogoal].[dbo].T_APP_SEEK_TREASURE_01
where fileguid is null and declare_date>='2018-01-01 00:00:00'
and declare_date<='2018-01-31 23:59:59'
--and seek_mark = '3'
and seek_mark >='4' AND seek_mark<='5'



select * from [gogoal].[dbo].T_APP_SEEK_TREASURE_01
order by entrydate desc



select count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH where Create_Date between'2018-01-01' and '2018-01-31'