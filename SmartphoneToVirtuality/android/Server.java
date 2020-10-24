import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.DatagramPacket;

import org.json.JSONObject;

public class Server {
    private ServerSocket serverSocket;
    private static final int port = 4269;

    public Server() {
        try {
            serverSocket = new ServerSocket(port);
            print_addr();
        }
        catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    private void print_addr() {
      try(final DatagramSocket socket = new DatagramSocket()){
        socket.connect(InetAddress.getByName("8.8.8.8"), 10002);
        System.out.println(socket.getLocalAddress().getHostAddress()+":"+port);
      }
      catch (Exception e) {
        e.printStackTrace();
      }
    }

    public void startTCP() {
      try {
        while(true) {
          BufferedReader in = new BufferedReader(new InputStreamReader(serverSocket.accept().getInputStream()));
          String l = in.readLine();
          process(l);
          if(l.equals("STOP")) break;
        }
        serverSocket.close();
      }
      catch (IOException ioe) {
          ioe.printStackTrace();
      }
    }

    public void startUDP() {
      try {
        DatagramSocket socket = new DatagramSocket(port);
        byte[] buf = new byte[256];
        while (true) {
              DatagramPacket packet = new DatagramPacket(buf, buf.length);
              socket.receive(packet);
              packet = new DatagramPacket(buf, buf.length, packet.getAddress(), packet.getPort());
              String received = new String(packet.getData(), 0, packet.getLength());
              received = received.substring(0, received.indexOf('\0'));
              process(received);
              if (received.equals("STOP")) break;
          }
          socket.close();
      }
      catch(Exception e) {
        e.printStackTrace();
      }
    }

    public void process(String s) {
      try {
        JSONObject json = new JSONObject(s);
        json.put("proximity", (Float.parseFloat(json.getString("proximity")) / 8)+"");
        String str = "accelerometer: "+json.getString("accelerometer")+" / ";
        str += "gyroscope: "+json.getString("gyroscope")+" / ";
        str += "proximity: "+json.getString("proximity");
        System.out.print('\r'+str+'\r');
      }
      catch (Exception e) {
        e.printStackTrace();
      }
    }

    public static void main(String[] args) {
      Server server = new Server();
      server.startUDP();
    }
}
