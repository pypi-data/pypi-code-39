#helping methods for sorting algorithms

def merge_list(array, start, mid, end):
        left = array[start:mid]
        right = array[mid:end]
        k = start
        i = 0
        j = 0
        while (start + i < mid and mid + j < end):
            if (left[i] <= right[j]):
                array[k] = left[i]
                i = i + 1
            else:
                array[k] = right[j]
                j = j + 1
            k = k + 1
        if start + i < mid:
            while k < end:
                array[k] = left[i]
                i = i + 1
                k = k + 1
        else:
            while k < end:
                array[k] = right[j]
                j = j + 1
                k = k + 1


def merge_sort(array, start, end):
    '''Sorts the list from indexes start to end - 1 inclusive.'''
    if end - start > 1:
        mid = (start + end)//2
        merge_sort(array, start, mid)
        merge_sort(array, mid, end)
        merge_list(array, start, mid, end)

    return array


def partition(arr,low,high): 
        i = low-1     # index of smaller element 
        pivot = arr[high]     # pivot 
        for j in range(low , high): 
    
            if   arr[j] <= pivot: 
                i = i+1 
                arr[i],arr[j] = arr[j],arr[i] 
    
        arr[i+1],arr[high] = arr[high],arr[i+1] 
        return ( i+1 ) 
    
    
def quick_sort(arr,first_index,last_index): 
    if first_index < last_index: 
        partition_index = partition(arr,first_index,last_index) 
        quick_sort(arr, first_index, partition_index-1) 
        quick_sort(arr, partition_index+1, last_index)

    return arr


def heapify(arr, n, i): 
    largest = i 
    l = 2 * i + 1     
    r = 2 * i + 2 

    if l < n and arr[i] < arr[l]: 
        largest = l 
  
    if r < n and arr[largest] < arr[r]: 
        largest = r 
   
    if largest != i: 
        arr[i],arr[largest] = arr[largest],arr[i] 
        heapify(arr, n, largest) 