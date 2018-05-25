# script to convert all files to 16bit integer
cd "problematic_submission_dir"

convert () {
  echo "$1";
  cd "$1";
  for i in *.wav;
    # get all stem filenames
    do name=`echo $i | awk -F".wav" '{$0=$1}1'`;
    # encode to AAC using Fraunhofer AAC encoding parameters
    ffmpeg -i $name.wav -sample_fmt s16 $name-16b.wav
    # sox $name.wav -b 16 $name-16b.wav
    rm $name.wav
    mv $name-16b.wav $name.wav
  done
  cd ..;
}

# encode to AAC
cd "test";
for dir in ./* ;do
  # iterate over track directories
  if [[ -d $dir ]];then
    convert "$dir";
  fi
done
