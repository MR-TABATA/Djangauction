from item.models import Item, Stat, Bid, BidHistory
from fee.models import Fee, UserFee
from accounts.models import CustomUser
import datetime

from django.http import JsonResponse
from django.urls import reverse_lazy, reverse


"""
#セカンドプライスオークション
1番手が2番手の金額で、落札できる
"""
def second_price_auction(self, form):
	stat_data = Stat.objects.select_related('item').filter(item_id=self.kwargs['pk'], deleted__isnull=True).first()
	if stat_data.item.close <= datetime.datetime.now():
		data = {
			'notice': 'オークションは終了しました',
		}
		return JsonResponse(data)
	else:
		stat_object = Stat.objects.get(pk=stat_data.pk)
		bid_price = form.cleaned_data.get('bid_price')
		bid_data = ()
		if bid_price <= stat_data.item.start_price:
			data = {
				'notice': 'フロア・プライスより、下の金額では入札できません',
			}
			return JsonResponse(data)
		unit = ['0', '5',]
		if not str(bid_price)[-3] in unit:
			data = {
				'notice': '上げ幅は 500円 単位です',
			}
			return JsonResponse(data)
		if stat_data.win_price == 0:
			bid = Bid(
				item_id=self.kwargs['pk'],
				bid_price=bid_price,
				custom_user_id=self.request.user.pk,
			)
			stat_object.bid_count = stat_object.bid_count + 1
			stat_object.win_price = stat_data.item.start_price
			stat_object.custom_user_id = self.request.user.pk

			bid_history = BidHistory(
				item_id=self.kwargs['pk'],
				history_price=stat_data.item.start_price,
				custom_user_id=self.request.user.pk,
			)

			# bid、bid_historyテーブルにデータ保存
			bid.save()
			bid_history.save()
			# statテーブルを更新
			stat_object.save()

			data = {
				# 'top_bidder': 'あなたです', #self.request.user.pk
				'bid_count': stat_object.bid_count + 1,
				'notice': "¥ " + str('{:,}'.format(bid_price)) + "まで、あなたがトップです",
				# 'win_price': "¥ " + str('{:,}'.format(stat_data.item.start_price)),
			}
			return JsonResponse(data)

		else:
			bid_first = Bid.objects.filter(item_id=self.kwargs['pk'], deleted__isnull=True).order_by('-bid_price',
																																															 'created', ).first()
			if self.request.user.pk == bid_first.custom_user_id:
				data = {
					'notice': '入札済みで、トップの場合は入札できません',
				}
				return JsonResponse(data)
			if bid_price <= stat_data.win_price:
				data = {
					'notice': 'トップ・プライスより、下の金額では入札できません',
				}
				return JsonResponse(data)
			else:
				if bid_price <= bid_first.bid_price:
					# bidテーブルにデータ保存
					bid = Bid(
						item_id=self.kwargs['pk'],
						bid_price=bid_price,
						custom_user_id=self.request.user.pk,
					)
					bid.save()
					bid_history = BidHistory(
						item_id=self.kwargs['pk'],
						history_price=bid_price,
						custom_user_id=stat_object.custom_user_id,
					)
					bid_history.save()
					stat_object.bid_count = stat_object.bid_count + 1
					stat_object.win_price = bid_price
					stat_object.custom_user_id = stat_object.custom_user_id
					stat_object.save()

					data = {
						'top_bidder': stat_object.custom_user_id,  # self.request.user.pk,
						'bid_count': stat_object.bid_count + 1,
						'notice': '残念、他の方がトップです',
						'win_price': "¥ " + str('{:,}'.format(bid_price)),
					}
					return JsonResponse(data)

				else:
					# bidテーブルにデータ保存
					bid = Bid(
						item_id=self.kwargs['pk'],
						bid_price=bid_price,
						custom_user_id=self.request.user.pk,
					)
					bid.save()

					if self.request.user.pk != stat_object.custom_user_id:
						win_price = bid_first.bid_price
					else:
						win_price = stat_object.win_price
					bid_history = BidHistory(
						item_id=self.kwargs['pk'],
						history_price=win_price,
						custom_user_id=self.request.user.pk,
					)
					bid_history.save()
					# statテーブルを更新
					stat_object.bid_count = stat_object.bid_count + 1
					stat_object.win_price = win_price
					stat_object.custom_user_id = self.request.user.pk
					stat_object.save()

					data = {
						'top_bidder': 'あなたです',
						'bid_count': stat_object.bid_count + 1,
						'notice': '¥ ' + str('{:,}'.format(bid_price)) + 'まで、あなたがトップです',
						'win_price': "¥ " + str('{:,}'.format(bid_first.bid_price)),
					}
					return JsonResponse(data)


"""
#ファーストプライスオークション
1番手が1番手の金額で、落札できる
"""
def first_price_auction(self, form):
	stat_data = Stat.objects.select_related('item').filter(item_id=self.kwargs['pk'], deleted__isnull=True).first()
	if stat_data.item.close <= datetime.datetime.now():
		data = {
			'notice': 'オークションは終了しました',
		}
		return JsonResponse(data)
	else:
		stat_object = Stat.objects.get(pk=stat_data.pk)
		bid_price = form.cleaned_data.get('bid_price')
		bid_data = ()
		if bid_price <= stat_data.item.start_price:
			data = {
				'notice': 'フロア・プライスより、下の金額では入札できません',
			}
			return JsonResponse(data)
		unit = ['0', '5', ]
		if not str(bid_price)[-3] in unit:
			data = {
				'notice': '上げ幅は 500円 単位です',
			}
			return JsonResponse(data)
		if stat_data.win_price == 0:
			bid = Bid(
				item_id=self.kwargs['pk'],
				bid_price=bid_price,
				custom_user_id=self.request.user.pk,
			)
			stat_object.bid_count = stat_object.bid_count + 1
			stat_object.win_price = bid_price
			stat_object.custom_user_id = self.request.user.pk

			# bidテーブルにデータ保存
			bid.save()
			# statテーブルを更新
			stat_object.save()

			data = {
				# 'top_bidder': 'あなたです', #self.request.user.pk
				'bid_count': stat_object.bid_count + 1,
				'notice': "¥ " + str('{:,}'.format(bid_price)) + "まで、あなたがトップです",
				# 'win_price': "¥ " + str('{:,}'.format(stat_data.item.start_price)),
			}
			return JsonResponse(data)

		else:
			bid_first = Bid.objects.filter(item_id=self.kwargs['pk'], deleted__isnull=True).order_by('-bid_price',
																																															 'created', ).first()
			if self.request.user.pk == bid_first.custom_user_id:
				data = {
					'notice': '入札済みで、トップの場合は入札できません',
				}
				return JsonResponse(data)
			if bid_price <= stat_data.win_price:
				data = {
					'notice': 'トップ・プライスより、下の金額では入札できません',
				}
				return JsonResponse(data)
			else:
				# bidテーブルにデータ保存
				bid = Bid(
					item_id=self.kwargs['pk'],
					bid_price=bid_price,
					custom_user_id=self.request.user.pk,
				)
				bid.save()

				# statテーブルを更新
				stat_object.bid_count = stat_object.bid_count + 1
				stat_object.win_price = bid_price
				stat_object.custom_user_id = self.request.user.pk
				stat_object.save()

				data = {
					'top_bidder': 'あなたです',
					'bid_count': stat_object.bid_count + 1,
					'notice': '¥ ' + str('{:,}'.format(bid_price)) + 'まで、あなたがトップです',
					'win_price': "¥ " + str('{:,}'.format(bid_first.bid_price)),
				}
				return JsonResponse(data)