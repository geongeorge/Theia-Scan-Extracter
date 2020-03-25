<div align="center">

<h1><img src="https://www.greekmythology.com/images/mythology/thea_26.jpg" width=48 style="border-radius: 50%;vertical-align:middle; margin-right: 8px;"> Theia</h1>

<div>
	<h3>
	Threshold and Extract Characters</h3>
</div>
</div>


## `i.py` : image thresholder

```bash
python i.py image.py [-s] [-t <num>] [-i <image.jpg>] [-o]
```

| flag | description | required | default |
|------|--------------|---------|---------|
| s | --sample : sample flag  | optional | false |
| t | --threshold: threshold value in &lt;num&gt; | required | _ |
| i | --image: Set image file to use | required  | _ |
| o | --out: split image into multiple parts as output | optional  | false |


### Instructions (sample)


**1.Show a sample**

    python i.py -i image.jpg -t 150 -s

**2. Adjust Threshold value till feels correct**

    python i.py -i image.jpg -t 130 -s

**3. Generate ouptuts**

    python i.py -i image.jpg -t 130 -o

**4. Manual check images, Copy ouput folders to corresponding locations, delete the op folder **

**5. Repeat with different image**



## Install

1. Install [Pipenv](https://github.com/pypa/pipenv)
2.     pipenv shell
3. Install required modules

        pipenv install 
