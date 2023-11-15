from item.models import Item, Stat
from fee.models import Fee, UserFee
from accounts.models import CustomUser
import datetime
from django.db.models import Sum, Count
from anymail.message import AnymailMessage

def maker_count(date):
	maker_count_sql = (" SELECT da_maker.id, da_maker.maker_name, count(da_item.id) AS count"
										 " FROM da_maker INNER JOIN da_item ON da_maker.id = da_item.maker_id "
										 " WHERE da_item.deleted is Null AND da_item.close >= %s "
										 " GROUP BY da_maker.id ORDER BY count DESC ")
	return Item.objects.raw(maker_count_sql, [date])

def calculated_bidding(custom_user_id, close):
	calculate = []
	sql = (
		" SELECT sum(da_stat.win_price) AS sum_win_price, count(da_stat.win_price) AS count_win_price, da_stat.custom_user_id,"
		" da_item.id, da_item.item_name, da_item.close, da_maker.maker_name"
		" FROM da_item, da_stat, da_maker"
		" WHERE da_item.id = da_stat.item_id"
		" AND da_item.maker_id = da_maker.id"
		" AND da_stat.custom_user_id = %s"
		" AND DATE_FORMAT(da_item.close, '%%Y-%%m-%%d') = %s"
		" GROUP BY da_stat.custom_user_id"
		" ORDER BY da_item.maker_id")
	summaries = Item.objects.raw(sql, [custom_user_id, close])

	sql = (
		" SELECT da_fee.* "
		" FROM da_fee inner join da_user_fee on da_user_fee.fee_id = da_fee.id "
		" WHERE "
		" da_fee.deleted IS NULL AND "
		" da_fee.`started` <= %s AND "
		" da_fee.`ended` >= %s AND "
		" da_user_fee.custom_user_id = %s ;"
	)
	fees = Fee.objects.raw(sql, [datetime.datetime.now(), datetime.datetime.now(), custom_user_id])
	win_count = 0
	for summary in summaries:
		win_sum = int(summary.sum_win_price)
		win_count = int(summary.count_win_price)
	bidding = 0
	for fee in fees:
		bidding = int(fee.bidding)

	calculate = {
		'sum_win_price':win_sum,
		'bidding_fee':win_count * bidding,
		'summaries':summaries,
		'bidding_unit_fee':bidding,
		'bidding_win_count':win_count,
		'bidding_total':win_sum+win_count * bidding,
	}

	return calculate


def calculated_commiting(custom_user_id, close):
	calculate = []

	summary = (
		Stat.objects.select_related('item').
		filter(deleted__isnull=True, item__custom_user_id=custom_user_id, item__close__date=close).
		values('id').aggregate(sum_win_price=Sum('win_price'))
	)

	#成約料
	commision = (
		Stat.objects.select_related('item').
		filter(item__deleted__isnull=True, item__custom_user_id=custom_user_id, item__close__date=close, win_price__gt=0).
		values('id').aggregate(count=Count('id'))
	)

	fee = (
		UserFee.objects.select_related('fee').
		filter(
			deleted__isnull=True,
			fee__started__lte=datetime.datetime.now(),
			fee__ended__gte=datetime.datetime.now(),
			custom_user_id=custom_user_id
		).first())

	# 成約料

	commision_fee = fee.fee.commission*commision['count']
	commision_count = commision['count']

	calculate = {
		'commision_fee':commision_fee,
		'commision_count':commision_count,
		'fee':fee,
		'summary': summary,
	}

	return calculate

def sendmailByBrevo(subject, body, to, bcc):
	message = AnymailMessage(
		subject=subject,
		body=body,
		to=[to],
		bcc=[bcc],
		tags=["Onboarding"],
	)

	return message

