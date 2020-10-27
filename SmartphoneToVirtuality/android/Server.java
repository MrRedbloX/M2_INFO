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
    private static int upd_count, count_per_second = 0;

    public Server() {
        try {
            serverSocket = new ServerSocket(port);
            print_addr();
            follow_updates();
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
              upd_count++;
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

    private void process(String s) {
      try {
        JSONObject json = new JSONObject(s);
        float proximity = Float.parseFloat(json.getString("proximity"));
        String str = upd_count+" upd/s - ";
        str += "accelerometer: "+json.getString("accelerometer")+" / ";
        str += "gyroscope: "+json.getString("gyroscope")+" / ";
        str += "proximity: "+json.getString("proximity");
        System.out.print('\r'+str+'\r');
      }
      catch (Exception e) {
        e.printStackTrace();
      }
    }

    private void follow_updates() {
      new Thread() {
        public void run() {
          while(true) {
            try {
              Thread.sleep(1000);
              count_per_second = upd_count;
              upd_count = 0;
            }
            catch(Exception e) {
              e.printStackTrace();
            }
          }
        }
      }.start();
    }

    public static void main(String[] args) {
      Server server = new Server();
      server.startUDP();
    }
}
