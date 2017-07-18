%data=dicominfo('D:\RouFiles\artemis\MATSUMU1\SEG2\SEG1');
%data=dicominfo('D:\RouFiles\artemis\SWINDEN_20170320081816_t2_tse_tra_HI_RES_PROSTATE_recent_change\SEG')

data1=dicomread('D:\RouFiles\artemis\SWINDEN_20170320081816_t2_tse_tra_HI_RES_PROSTATE_recent_change\SEG');
%%
segmentData=data.SegmentSequence.Item_1;