# -*- coding: UTF-8 -*-

#Reverse Text
def revtext(text):
 return text[::-1]

#Reverse Array
def revarray(array):
  return array[::-1]

def bsearch(_list, target):
 if type(_list) is not list:
    raise TypeError("binary search only excepts lists, not {}".format(str(type(_list))))

# First position of the list
 left = 0
# Last position of the list
 right = len(_list) - 1

 try:
    # you can also write while True condition
    while left <= right:
        mid = (left + right) // 2
        if target == _list[mid]:
            return mid
        elif target < _list[mid]:
            right = mid - 1
        else:
            left = mid + 1
    return False
 except TypeError:
    return False

def revowel(s):
    vowels = "AEIOUaeiou"
    i, j = 0, len(s)-1
    s = list(s)
    while i < j:
        while i < j and s[i] not in vowels:
            i += 1
        while i < j and s[j] not in vowels:
            j -= 1
        s[i], s[j] = s[j], s[i]
        i, j = i + 1, j - 1
    return "".join(s)

def samewords(strs):
    '''
["eat", "tea", "tan", "ate", "nat", "bat"],
#Output : [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
    '''
    d = {}
    ans = []
    k = 0
    for str in strs:
        sstr = ''.join(sorted(str))
        if sstr not in d:
            d[sstr] = k
            k += 1
            ans.append([])
            ans[-1].append(str)
        else:
            ans[d[sstr]].append(str)
    return ans


def dprint(dictionary):
    for index in dictionary.keys():
        print "{} : {}".format(index,dictionary[index])


def spattern(pattern, string):
    """
    :type pattern: str
    :type string: str
    :rtype: bool
    """
    def backtrack(pattern, string, dic):

        if len(pattern) == 0 and len(string) > 0:
            return False

        if len(pattern) == len(string) == 0:
            return True

        for end in range(1, len(string)-len(pattern)+2):
            if pattern[0] not in dic and string[:end] not in dic.values():
                dic[pattern[0]] = string[:end]
                if backtrack(pattern[1:], string[end:], dic):
                    return True
                del dic[pattern[0]]
            elif pattern[0] in dic and dic[pattern[0]] == string[:end]:
                if backtrack(pattern[1:], string[end:], dic):
                    return True
        return False

    return backtrack(pattern, string, {})


def permute(elements):
    """
        iterator: returns a perumation by each call.
    """
    if len(elements) <= 1:
        yield elements
    else:
        for perm in permute_iter(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]

def upermute(nums):
    perms = [[]]
    for n in nums:
        new_perms = []
        for l in perms:
            for i in range(len(l)+1):
                new_perms.append(l[:i]+[n]+l[i:])
                if i < len(l) and l[i] == n:
                    break  # handles duplication
        perms = new_perms
    return perms



def genabbrev(word):
    def backtrack(result, word, pos, count, cur):
        if pos == len(word):
            if count > 0:
                cur += str(count)
            result.append(cur)
            return
        if count > 0:  # add the current word
            backtrack(result, word, pos+1, 0, cur+str(count)+word[pos])
        else:
            backtrack(result, word, pos+1, 0, cur+word[pos])
        # skip the current word
        backtrack(result, word, pos+1, count+1, cur)
    result = []
    backtrack(result, word, 0, 0, "")
    return result


def lettercombin(digits):
    if digits == "":
        return []
    kmaps = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz"
    }
    ans = [""]
    for num in digits:
        tmp = []
        for an in ans:
            for char in kmaps[num]:
                tmp.append(an + char)
        ans = tmp
    return ans
