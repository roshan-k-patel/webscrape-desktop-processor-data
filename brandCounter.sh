line=$1
IFS=','

intel=0
amd=0
other=0

otherList=""

while read line
do
	arr=($line)

	if [ "$arr" == "Intel" ]
	then 
		((intel++))
	elif [ "$arr" == "AMD" ]
	then 
		((amd++))
        elif [ "$arr" == "Brand" ]
	then
		echo""
	else
		((other++))

	fi

done < "${1:-/dev/stdin}" 

echo "Processor Brand Count:"
echo "Intel: $intel"
echo "AMD: $amd"
echo "Other (White Label): $other"

