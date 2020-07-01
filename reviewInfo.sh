line=$1
IFS=','

intel=0
intelLines=0

amd=0
amdLines=0

other=0
otherLines=0

totalLines=0
while read line
do
	((totalLines++))
	arr=($line)
	
	if [ "$arr" == "Intel" ]
	then 
		((intel=intel+${arr[5]}))
		((intelLines++))
	elif [ "$arr" == "AMD" ]
	then 
		((amd=amd+${arr[5]}))
		((amdLines++))
        elif [ "$arr" == "Brand" ]
	then
		((totalLines--))
	else
		((other=other+${arr[5]}))
		((otherLines++))
	fi
done < "${1:-/dev/stdin}"

totalReviews=$(((intel+amd+other)))

echo "Total Reviews: $totalReviews"
echo "Total Items: $totalLines"
echo ""

echo "Average No. Of Reviews"
echo "Avg for all: $((totalReviews/totalLines))"
echo "Intel: $((intel/intelLines))"
echo "AMD: $((amd/amdLines))"

if [ $otherLines==0 ] 
then 
	echo""
else
	echo "Other (White Label): $((other/otherLines))"
fi

echo "Percentage of All Reviews"
amdPercent=$(((amd*100)/totalReviews))

echo "Intel: $(((intel*100)/totalReviews))%"
echo "AMD: $(((amd*100)/totalReviews))%" 

if [ $otherLines==0 ]
then
        echo""
else
	
	echo "Other (White Label): $(((other*100)/totalReviews))%"
fi

