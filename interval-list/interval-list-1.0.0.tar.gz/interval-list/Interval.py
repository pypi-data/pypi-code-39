class Interval:
	def __init__(self, _min, _max, *args, **kwargs):
		if type(_min) != type(_max):
			raise TypeError("min({})とmax({})のタイプが異なっています。".format(type(_min), type(_max)))

		if _min > _max:
			raise ValueError("min > max となっています。", "min:", _min, " max:", _max)
		elif _min == _max:
			kwargs.setdefault("ignore", False)
			if kwargs["ignore"]:
				pass
			# else:
			# 	warnings.warn("min == max となっています。min,max: " + str(_min))

		self.min = _min
		self.max = _max

	def __min__(self):
		return self.min

	def __max__(self):
		return self.max

	# str(self)
	def __str__(self):
		"""return "min ~ max" """
		return "{min} ~ {max}".format(min=str(self.min), max=str(self.max))

	def __repr__(self):
		cls_name = self.__class__.__name__
		return cls_name + "(" + repr(self.min) + ", " + repr(self.max) + ")"

	# self and other
	def __and__(self, other):
		if self.max < other.min or self.min > other.max:
			return None
		else:
			_min = max(self.min, other.min)
			_max = min(self.max, other.max)
			return Interval(_min, _max)

	def __getitem__(self, item):
		if item == 0:
			return self.min
		elif item == 1:
			return self.max
		else:
			raise IndexError("indexは０または１を指定して下さい。(入力値：{})".format(item))

	# bool(self)
	def __bool__(self):
		return True

	# self or other
	def __or__(self, other):
		if self.max < other.min or self.min > other.max:
			if self.max < other.min:
				return Intervals((self, other))
			else:
				return Intervals((other, self))
		else:
			_min = min(self.min, other.min)
			_max = max(self.max, other.max)
			return Interval(_min, _max)

	# self == other
	def __eq__(self, other):
		if self.min == other.min and self.max == other.max:
			return True
		else:
			return False

	# self != other
	def __ne__(self, other):
		return not self == other

	# self < other
	def __lt__(self, other):
		if self.min > other.min and self.max < other.max:
			#  other.min < self.min < self.max < other.max
			return True
		else:
			return False

	# self > other
	def __gt__(self, other):
		"""self > other"""
		return other < self

	# self <= other
	def __le__(self, other):
		if self.min >= other.min and self.max <= other.max:
			return True
		else:
			return False

	# self >= other
	def __ge__(self, other):
		return other <= self

	# item in self
	def __contains__(self, item):
		if item.__class__.__name__ == "interval-list":
			return self > item
		elif item.__class__.__name__ == "Intervals":
			item.marge()
			item_interval = Interval(item[0].min, item[-1].max)
			return self > item_interval
		elif isinstance(item, type(self.min)):
			return self.min <= item <= self.max
		else:
			raise TypeError("item must be interval-list or Intervals. (got ", item.__class__.__name__, " class)")


class Intervals:

	def __init__(self, intervals=()):

		new_intervals = list(intervals)
		for index, interval in enumerate(intervals):
			new_intervals[index] = self.check_interval(interval)
		self.Intervals = new_intervals

	@staticmethod
	def check_interval(interval):
		if isinstance(interval, Interval):
			pass
		elif type(interval) == list:
			if len(interval) != 2:
				raise IndexError("if you create Intervals with list, the elements's length must be 2.")
			else:
				interval = Interval(interval[0], interval[1], ignore=True)
		else:
			raise TypeError(
				"the arguments's element must be list or interval-list.(we recommend interval-list because list is change to interval-list.)")
		return interval

	def __getitem__(self, item):
		return self.Intervals[item]

	def sort(self, *, reverse: bool = ...) -> None:
		if reverse:
			key = Interval.__max__
		else:
			key = Interval.__min__
		self.Intervals.sort(key=key)

	def __str__(self) -> str:
		str_interval = [str(interval) for interval in self.Intervals]
		return "[" + ", ".join(str_interval) + "]"

	def __repr__(self) -> str:
		cls_name = self.__class__.__name__
		argument = "(" + ", ".join([repr(interval) for interval in self.Intervals]) + ")"
		return cls_name + "(" + argument + ")"

	def marge(self):
		self.sort()
		copy = []
		append = copy.append

		for index, interval in enumerate(self.Intervals):
			if index == 0:
				append(interval)
				continue
			else:
				pass
			interval1 = copy[-1]
			# copyの最後のInterval
			interval2 = interval
			if interval1 & interval2:
				# 共通部分があるなら
				copy[-1] = interval1 | interval2
			else:
				append(interval2)
		self.Intervals = copy

	def append(self, interval):
		interval = self.check_interval(interval)
		self.Intervals.append(interval)

	def __len__(self):
		return len(self.Intervals)

	# item in self
	def __contains__(self, item):
		if isinstance(item, Interval):
			self.marge()
			min_index, max_index = None, None
			for index, interval in enumerate(self.Intervals):
				if item.min in interval:
					min_index = index
				if item.max in interval:
					max_index = index
			if min_index is not None and max_index is not None and min_index == max_index:
				return True
			else:
				return False
		if isinstance(item, Intervals):
			item.marge()
			for interval in item:
				if interval not in self:
					return False
			return True
