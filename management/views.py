import datetime

from django.shortcuts import render
from django.views.generic import CreateView, FormView, ListView
from .mixins import SuperuserRequiredMixin

from django.db.models import F
from django.db.models import Sum, Count

from item.models import Item, Stat
from fee.models import Fee, Offset, UserFee, Tax
from accounts.models import CustomUser

from django.core.files.storage import FileSystemStorage
from config.consts import PHOTO_FILE_PATH

import math


#画像アップロード
class UploadImageView(SuperuserRequiredMixin, FormView) :
	def get(self, request, *args, **kwargs):
		context = {}
		context['crumbs'] = [
			['画像アップロード', 'management:upload_image'],
		]
		context['title'] = '画像アップロード'

		return render(request, 'management/apply/upload_image.html', context)

	def post(self, request):
		context = {}
		context['title'] = 'Auction Management 画像アップロード'
		images = request.FILES.getlist('image')
		fss = FileSystemStorage(location=PHOTO_FILE_PATH)
		for image in images:
			file = fss.save(image.name, image)

		return render(request, 'management/apply/upload_image.html', context)

class CloseView(SuperuserRequiredMixin, ListView):
	def get(self, request, *args, **kwargs):
		context = {}
		context['crumbs'] = [
			['終了日一覧', 'management:close'],
		]
		context['title'] = '終了日一覧'

		context['auction_closes'] = Item.objects.values_list('close').filter(deleted__isnull=True, close__lt=datetime.datetime.now()).order_by('-close').distinct()

		return render(request, 'management/report/close.html', context)

class ReportView(SuperuserRequiredMixin, ListView):
	def get(self, request, *args, **kwargs):
		context = {}
		context['crumbs'] = [
			['終了日一覧', 'management:close'],
			['相殺', ''],
		]
		context['title'] = '相殺表'
		context['unixtime'] = self.kwargs['unixtime']
		close_datetime = datetime.datetime.fromtimestamp(self.kwargs['unixtime'])
		item_close = Item.objects.filter(deleted__isnull=True, close=close_datetime ).order_by('-close').first()
		#stats = (
		#	Stat.objects.select_related('item').values('custom_user').
		#	annotate(sum=Sum('win_price'), count=Count('pk')).
		#	filter(deleted__isnull=True, item__close=item_close.close).
		#	exclude(custom_user__lt=10)
		#)
		sql=(" SELECT da_stat.id, da_stat.custom_user_id, sum(da_stat.win_price) AS sum, count(da_stat.id) AS count FROM da_stat "
				 " INNER JOIN da_item ON da_stat.item_id = da_item.id "
				 " WHERE da_stat.deleted IS NULL "
				 " AND   da_item.close = %s "
				 " AND   da_stat.custom_user_id >= 10 "
				 " AND   da_stat.win_price > %s "
				 " GROUP BY da_stat.custom_user_id ")
		stats = Stat.objects.raw(sql, [item_close.close, 0, ])

		is_offsets = Offset.objects.filter(deleted__isnull=True, close=item_close.close).values('id')
		offset_obj = []
		for is_offset in is_offsets:
			offset_obj = Offset.objects.get(pk=is_offset['id'])
			offset_obj.deleted=datetime.datetime.now()
			offset_obj.save()
		offset_obj = []
		for stat in stats:
			user_fee = UserFee.objects.filter(custom_user=stat.custom_user_id).exclude(custom_user__lt=10).values('fee').first()
			fee=(
				Fee.objects.filter(id=user_fee['fee'], started__lte=datetime.datetime.now(), ended__gte=datetime.datetime.now()).
				values('commission', 'bidding', 'bidding_margin', 'commission_margin', ).first()
			)
			if fee['bidding_margin']:
				bidding_fee_sum = fee['bidding_margin'] * stat.sum
			else:
				bidding_fee_sum = fee['bidding'] * stat.count

			offset_obj.append(Offset(
				custom_user=CustomUser.objects.get(id=stat.custom_user_id),
				fee=Fee.objects.get(id=user_fee['fee']),
				close=item_close.close,
				bidded_sum=stat.sum,
				bidding_count=stat.count,
				bidding_fee_sum=bidding_fee_sum,
			))
		Offset.objects.bulk_create(offset_obj)

		#落札しているユーザーの成約データのupdate
		offsets = Offset.objects.filter(deleted__isnull=True, close=item_close.close).values('custom_user')
		for offset in offsets:
			sql = ''
			sql = (
				" SELECT da_stat.id, da_item.custom_user_id, sum(da_stat.win_price) AS sum, count(da_stat.id) AS count FROM da_stat "
				" INNER JOIN da_item ON da_stat.item_id = da_item.id "
				" WHERE da_stat.deleted IS NULL "
				" AND   da_item.close = %s "
				" AND   da_item.custom_user_id = %s "
				" AND   da_stat.win_price > %s "
				" GROUP BY da_item.custom_user_id ")
			stats = Stat.objects.raw(sql, [item_close.close, offset['custom_user'], 0, ])

			if stats:
				for stat in stats:
					if fee['commission_margin']:
						commission_fee_sum = fee['commission_margin'] * stat.sum
					else:
						commission_fee_sum = fee['commission'] * stat.count
					offset_obj = []
					offset = Offset.objects.filter(deleted__isnull=True, close=item_close.close, custom_user=stat.custom_user_id).values('id').first()
					offset_obj = Offset.objects.get(pk=offset['id'])
					offset_obj.commission_count=stat.count
					offset_obj.commission_fee_sum=commission_fee_sum
					offset_obj.commissioned_sum=stat.sum
					offset_obj.save()

		#ここで、成約のみインサートするが、すでにoffsetテーブルに値がある場合は除く
		items = (
			Stat.objects.select_related('item').
			filter(deleted__isnull=True, win_price__gt=0, item__close=item_close.close).
			values('item__custom_user').
			annotate(count=Count('item__custom_user'), sum=Sum('win_price'))
		)
		for item in items:
			if item is not None:
				user_fee = UserFee.objects.filter(custom_user=item['item__custom_user']).values('fee').first()
				#offsetテーブルに値がある場合は除く
				offset=Offset.objects.filter(deleted__isnull=True, close=item_close.close, custom_user=item['item__custom_user']).first()
				if not offset:
					offset_obj = []
					if user_fee:
						offset_obj = Offset(
							close=item_close.close,
							fee=Fee.objects.get(id=user_fee['fee']),
							commission_count=item['count'],
							commission_fee_sum=fee['commission'] * item['count'],
							custom_user=CustomUser.objects.get(id=item['item__custom_user']),
							commissioned_sum=item['sum'],
						)
						offset_obj.save()

		context['offsets'] = Offset.objects.select_related('custom_user').filter(deleted__isnull=True, close=close_datetime)
		return render(request, 'management/report/report_index.html', context)


class InvoiceView(SuperuserRequiredMixin, ListView):

	def get(self, request, *args, **kwargs):
		context = {}

		close_datetime = datetime.datetime.fromtimestamp(self.kwargs['unixtime'])

		bidding_stats=(
			Stat.objects.select_related('item', 'custom_user', 'item__maker').
			values(
				'item__custom_user', 'item__code', 'item__item_name', 'item__serial', 'item__maker__maker_name', 'item__close',
				'custom_user__company_name', 'win_price', 'custom_user'
			).
			filter(item__close=close_datetime, custom_user=self.kwargs['custom_user_pk'], win_price__gt=0).
		  exclude(item__custom_user=self.kwargs['custom_user_pk']).
			order_by('-custom_user', 'item__maker')
		)
		bidding_sum=0
		for bidding_stat in bidding_stats:
			bidding_sum +=bidding_stat['win_price']

		committing_stats = (
			Stat.objects.select_related('item', 'custom_user', 'item__maker').
			values(
				'item__custom_user', 'item__code', 'item__item_name', 'item__serial', 'item__maker__maker_name', 'item__close',
				'custom_user__company_name', 'win_price', 'custom_user'
			).
			filter(item__close=close_datetime, item__custom_user=self.kwargs['custom_user_pk'], win_price__gt=0).
			order_by('-custom_user', 'item__maker')
		)
		committing_sum=0
		for committing_stat in committing_stats:
			committing_sum +=committing_stat['win_price']

		user_fee=(
			UserFee.objects.select_related('fee').
			values('fee__bidding', 'fee__bidding_margin', 'fee__commission', 'fee__commission_margin').
			filter(
				deleted__isnull=True,
				fee__started__lte=close_datetime,
				fee__ended__gt=close_datetime,
				custom_user=self.kwargs['custom_user_pk']
			).first())

		tax = (
			Tax.objects.values('tax_rate',).
			filter(
				deleted__isnull=True,
				started__lte=close_datetime,
				ended__gt=close_datetime,
			).first())

		stats=bidding_stats | committing_stats
		context['bidding_count'] = len(bidding_stats)
		context['user_fee'] = user_fee
		context['bidding_sum'] = bidding_sum
		context['bidding_fee'] = len(bidding_stats) * user_fee['fee__bidding']
		context['bidding_total'] = bidding_sum + len(bidding_stats) * user_fee['fee__bidding']
		context['commiting_count'] = len(committing_stats)
		context['commiting_sum'] = committing_sum
		context['commiting_fee'] = len(committing_stats) * user_fee['fee__commission']
		context['commiting_total'] = committing_sum + len(committing_stats) * user_fee['fee__commission']
		if context['commiting_total'] >= context['bidding_total']:
			context['offset_total'] = context['commiting_total']-context['bidding_total']
		else:
			context['offset_total'] = context['bidding_total'] - context['commiting_total']
		context['tax_price'] = math.floor(context['offset_total'] * tax['tax_rate'])

		context['invoice_price'] = context['offset_total'] + math.floor(context['offset_total'] * tax['tax_rate'])

		context['page']=math.ceil(len(stats)/15)
		context['stats'] = stats

		context['auction_user'] = CustomUser.objects.filter(id=self.kwargs['custom_user_pk']).first()

		return render(request, 'management/report/invoice.html', context)


class OnItemView(SuperuserRequiredMixin, ListView):

	def get(self, request, *args, **kwargs):
		context = {}
		context['crumbs'] = [
			['Home', 'management:close'],
		]
		context['title'] = '開催中一覧'
		close_datetime = Item.objects.values('close').filter(deleted__isnull=True, close__gte=datetime.datetime.now()).order_by('-id').first()
		stats = ()
		if close_datetime is not None:
			sql = (" SELECT max(da_bid.bid_price) AS max, da_stat.win_price, da_stat.custom_user_id,"
						 " da_item.id, da_item.item_name, da_item.maker_id, da_item.close, da_maker.maker_name"
						 " FROM da_item, da_bid, da_stat, da_maker"
						 " WHERE da_bid.item_id = da_item.id"
						 " AND da_item.id = da_stat.item_id"
						 " AND da_item.id = da_bid.item_id"
						 " AND da_item.maker_id = da_maker.id"
						 " AND da_item.close = %s"
						 " GROUP BY da_stat.win_price, da_stat.custom_user_id, da_item.id, da_item.item_name,"
						 " da_item.maker_id, da_item.close"
						 " ORDER BY da_item.maker_id")
			context['items'] = Item.objects.raw(sql, [close_datetime['close']])


			context['stats'] = (
				Stat.objects.
				values(
					'item_id', 'item__custom_user__company_name', 'item__code', 'item__item_name', 'item__serial', 'item__start_price',
					'item__maker__maker_name', 'item__close','custom_user__company_name', 'win_price', 'custom_user',
				).
				filter(item__close=close_datetime['close']).order_by('-custom_user', 'item__maker', )
			)



		return render(request, 'management/item/on_item.html', context)