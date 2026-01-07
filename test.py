import sys
k = int(input())
s = input().replace('\n','')
s = " " + s
c = [0] * 1000002
c[0] = 1
t = ans = 0
for i in range(1,len(s)):
    t = t + (ord(s[i]) - 48)
    if (t >= k): ans = ans + c[t - k]
    c[t] += 1
print(ans)