# asciiviewer

A pretty viewer for XSM files generated by DRAGON/DONJON or APOLLO neutronic codes

As a DRAGON or DONJON user, you want to look inside a LCM object 
(LINKED_LIST, SEQ_ASCII or XSM_FILE). 
The simplest way to do this is to convert your object in `XSM_FILE` or `SEQ_ASCII` format :

    XSM_FILE myXsmFile ; myXsmFile := myLCMObject ;

Open the resulting file with __asciiviewer__ and you'll be able to 
browse through it thanks to a treeview.
