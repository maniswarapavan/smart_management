#!/usr/bin/python
import sys
import re

## VARS
## Set slide prefix, the prefix will start each slide name
slide_prefix="m"
## All slides file name, don't change this
index_file_name="AllSlides.txt"
    ## Setting headers
headers = """
:scrollbar:
:data-uri:
:noaudio:
"""



## Main function, this will split a source file into slides
def main(argv):
    print("Processing file: ",sys.argv[1])
    print("File Destination Directory:",sys.argv[2])
    ## Open source module file
    module_file = open(sys.argv[1],'rb')
    ## Set destination directory
    target_dir=sys.argv[2]
    ## Open Index File
    index_file=open(target_dir + "/" + index_file_name,'w')
    ## Reset slide count
    slide_number = 0
    ## go through the file line by line
    ## in case a new slide is found ("^== "), create a new slide
    ## in case the line is a header line (:something:), ignore it
    ## in case line is a regular line, just write it into the current slide
    for line in module_file:
        slide_name_line = re.compile("^==[^=](.*)")
        slide_header_line = re.compile("(^:.*:$)")
        # Check if the line is a new "slide name" line ("^== "),
        if slide_name_line.match(line):
            slide_number=slide_number+1
            # This is a work around for "title slides"
            if "nbsp" in line:
                print "found title slide"
                new_slide_name=str(slide_prefix + "01_Title.adoc")
            # If the next lines are not part of a title slide
            else:
                print("Found New Slide name",slide_name_line.match(line).group(1))
                # Create new slide name from slide number and slide name
                new_slide_name=str(0) + str(1) + "s" + str(slide_number) + " " + str(slide_name_line.match(line).group(1)) + ".adoc"
                # replace all spaces with underscores
                new_slide_name=new_slide_name.replace(' ','_')
                # replace "-" with nothing
                new_slide_name=new_slide_name.replace('-_','')
                # Add 0 for slides numbered less than 10
                if slide_number < 10:
                    new_slide_name= "0" +new_slide_name
                # Add slide prefix to slide
                new_slide_name = slide_prefix + new_slide_name
            # Open the new slide
            new_slide=open(target_dir + "/" + new_slide_name,"w")
            # Populate index file with slide name
            index_file.write("include::" + new_slide_name + "[]\n")
            # inject slide headers at the beginning of the slide
            new_slide.write(headers)
            # write slide name into slide file
            new_slide.write(line)
        # ignore header lines (":whatever:")
        elif slide_header_line.match(line):
            print("Found a header line to ignore",slide_header_line.match(line).group(1))
        # Write regular lines into the slide file
        else:
            new_slide.write(line)



if __name__ == "__main__":
   main(sys.argv[1:])

