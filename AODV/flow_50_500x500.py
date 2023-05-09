from xml.etree import ElementTree as ET
import sys
import matplotlib.pyplot as pylab
et=ET.parse(sys.argv[1])
bitrates=[]
losses=[]
delays=[]
for flow in et.findall("FlowStats/Flow"):
	for tpl in et.findall("Ipv4FlowClassifier/Flow"):
		if tpl.get('flowId')==flow.get('flowId'):
			break
	if tpl.get('destinationPort')=='654':
		continue
	losses.append(int(flow.get('lostPackets')))
	
	rxPackets=int(flow.get('rxPackets'))
	if rxPackets==0:
		bitrates.append(0)
	else:
		t0=float(flow.get('timeFirstRxPacket')[:-2])
		t1=float(flow.get("timeLastRxPacket")[:-2])
		duration=(t1-t0)*1e-9
		bitrates.append(8*int(flow.get("rxBytes"))/duration*1e-3)
		delays.append(float(flow.get('delaySum')[:-2])*1e-9/rxPackets)

pylab.subplot(311)
pylab.hist(bitrates,bins=40)
pylab.xlabel("Flow Bit Rates (b/s)/Cкорость передачи данных")
pylab.ylabel("Number of Flows/Kоличество потоков")

pylab.subplot(312)
pylab.hist(bitrates,bins=40)
pylab.xlabel("Number of Lost Packets/Количество потерянных пакетов")
pylab.ylabel("Number of Flows/Количество потоков")

pylab.subplot(313)
pylab.hist(bitrates,bins=10)
pylab.xlabel("Delay in Seconds/Задержка(сек)")
pylab.ylabel("Number of Flows/Количество потоков")

pylab.subplots_adjust(hspace=0.46)
pylab.savefig("AODV_50_500x500.pdf")
