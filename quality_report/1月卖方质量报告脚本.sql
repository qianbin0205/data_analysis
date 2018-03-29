--�������ֲ����
--154 ReportDB

--A��
--select count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
--where create_date between'2018-01-01 00:00:00.000' and '2018-01-30 00:00:00.000' and report_type_id<>'28'


select left(CONVERT(varchar(100), create_date, 112),6),count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
where  right(CONVERT(varchar(100), create_date, 12),4) between 0101 and 0130 and report_type_id<>'28'
and year(create_date) between 2013 and 2018
group by left(CONVERT(varchar(100), create_date, 112),6)
order by left(CONVERT(varchar(100), create_date, 112),6)

--H��
--select count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
--where create_date between'2017-11-01 00:00:00.000' and '2017-11-30 00:00:00.000' and report_type_id='28'


select left(CONVERT(varchar(100), create_date, 112),6),count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT_RESEARCH
where  right(CONVERT(varchar(100), create_date, 12),4) between 0101 and 0130 and report_type_id='28'
and year(create_date) between 2013 and 2018
group by left(CONVERT(varchar(100), create_date, 112),6)
order by left(CONVERT(varchar(100), create_date, 112),6)
--�Ǹ���
--select count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT
--where create_date between'2018-01-01 00:00:00.000' and '2018-01-31 00:00:00.000'


select left(CONVERT(varchar(100), create_date, 112),6),count(*) from [192.168.0.154].[reportdb].dbo.T_II_REPORT
where  right(CONVERT(varchar(100), create_date, 12),4) between 0101 and 0131
and year(create_date) between 2013 and 2018
group by left(CONVERT(varchar(100), create_date, 112),6)
order by left(CONVERT(varchar(100), create_date, 112),6)


--��ҵ����������ҵ�ķֲ����
--0.154
--Ϊ�յ��޳�
select top 10 industry,count(*) as cnt from [192.168.0.154].[reportdb].dbo.T_RPT_BROWSER a
join report_type b 
on a.report_type_id=b.reporttypeid
where b.reporttypeid in (15,16,17,18,19,20) and 
industry <> '' and
create_date between'2018-01-01 00:00:00.000' and '2018-01-31 00:00:00.000'
group by industry 
order by count(*) desc



--��6����ҵ�ϰ����
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

--ҵ��Ԥ�桢�챨����ʱ��
--0.11  gogoal
--�����������洦��ʱ�ԣ��޳���
--��������192.168.0.11  ���ݿ⣺gogoal
/****** Script for SelectTopNRows command from SSMS  ******/
--ץȡʱ��
drop table #trsgg,#tmp1,#4

SELECT
[hkey],
lasttime
  into #trsgg
FROM [192.168.0.153].[TRS_Results_Express].[dbo].[urlcontent]
--�챨ԭʼ drop table #tmp1
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
--Ԥ��ԭʼ
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
a.bs ��������,
a.guid,
a.publish_date �޳�ʱ��,
t.lasttime ץȡʱ��,
case when (datepart(hh,a.publish_date)!= 0 or datepart(mi,a.publish_date)!= 0 or datepart(ss,a.publish_date)!= 0)then a.publish_date
else t.lasttime end ����ʱ��,
a.entrytime ¼��ʱ��
into #4
from #tmp1 a
left outer join #trsgg t
on a.hkey=t.hkey



--------------�ǹ���ʱ�� ---------------------------------------------
select ��������,count(*) �ǹ���ʱ�� from #4 
where ����ʱ�� is not null and ����ʱ��>='2018-01-01 00:00:00'
and (DATEPART(hh, ����ʱ��)  <= 9 or DATEPART(hh, ����ʱ��) >= 21  or datepart(dw,����ʱ��) in (1,7))
group by ��������

----------------����ʱ��---------------------------------------------
--����ʱ�� <= 30 mins
select �������� ,count(*) '����ʱ��<=30' from #4 
where ����ʱ�� is not null and ����ʱ��>='2018-01-01 00:00:00'
and datediff(minute, ����ʱ��, ¼��ʱ��) <= 30
and (DATEPART(hh, ����ʱ��)  >  9 or DATEPART(hh, ����ʱ��) < 21)
and datepart(dw,����ʱ��) not in (1,7)
group by ��������

--����ʱ�� > 30 mins
select ��������,count(*) '����ʱ��>30' from #4 
where ����ʱ�� is not null and ����ʱ��>='2018-01-01 00:00:00'
and datediff(minute, ����ʱ��, ¼��ʱ��) > 30
and (DATEPART(hh, ����ʱ��)  >  9 or DATEPART(hh, ����ʱ��) < 21)
and datepart(dw,����ʱ��) not in (1,7)
group by ��������

--�ֲ����
select �������� as rpt_type,'01-' + cast(DATEPART(dd, ����ʱ��) as varchar(10)) as date,count(*) as cnt ,cast(cast(max(datediff(minute, ����ʱ��, ¼��ʱ��)) as float)/60 as decimal(10,2)) as hours from #4 
where ����ʱ�� is not null and ����ʱ��>='2018-01-01 00:00:00'
and datediff(minute, ����ʱ��, ¼��ʱ��) > 30
and DATEPART(hh, ����ʱ��)  between 9 and 21
and datepart(dw,����ʱ��) not in (1,7)
group by ��������,cast(DATEPART(dd, ����ʱ��) as varchar(10)),DATEPART(dd, ����ʱ��)
order by ��������,DATEPART(dd, ����ʱ��)

--��������
select * from #4



select * , datediff(minute, ����ʱ��, ¼��ʱ��) /60.0 from #4 
where ����ʱ�� is not null and ����ʱ��>='2018-01-01 00:00:00'
and datediff(minute, ����ʱ��, ¼��ʱ��) > 30
and (DATEPART(hh, ����ʱ��)  >  9 and DATEPART(hh, ����ʱ��) < 21)
and datepart(dw,����ʱ��) not in (1,7)
order  by ����ʱ�� ,¼��ʱ�� desc



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

--��Ԥ��Ѱ������ռ�����
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