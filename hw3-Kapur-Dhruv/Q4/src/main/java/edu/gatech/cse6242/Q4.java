package edu.gatech.cse6242;

import java.io.IOException;
import java.lang.Object;
import java.util.StringTokenizer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import org.apache.log4j.Logger;

public class Q4 {

	static Logger log = Logger.getLogger(Q4.class.getName());


    public static class DiffMapper
       extends Mapper<Object, Text, IntWritable, IntWritable>{
    private final static IntWritable src = new IntWritable(); // type of output value
    private IntWritable tgt = new IntWritable();  // type of output key
    private IntWritable one = new IntWritable(1);
    private IntWritable negone = new IntWritable(-1);
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      try {
      StringTokenizer itr = new StringTokenizer(value.toString(),"\n"); // line to string token
      while (itr.hasMoreTokens()) {
        String str = itr.nextToken();
        String[] tokens = str.split("\\t");
        log.info(tokens.toString());
        System.out.println(tokens.toString());
        src.set(Integer.parseInt(tokens[0]));
        tgt.set(Integer.parseInt(tokens[1])); 
        //System.out.println(Integer.parseInt(tokens[0]));
        // set word as each input keyword
        context.write(src,negone);
        context.write(tgt,one);    
        }
      }
        catch(Exception e)
        {System.out.print(e.getLocalizedMessage());
        }
      
    }
  }

  public static class DiffReducer
  extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
  private IntWritable result = new IntWritable();
  @Override
  public void reduce(IntWritable key, Iterable<IntWritable> values,Context context
                       ) throws IOException, InterruptedException {
      int diff = 0;
      int sum = 0; 
      for (IntWritable val : values) {
             
        	sum +=val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
   }

    public static class FreqMapper
    extends Mapper<Object, Text, IntWritable, IntWritable>{
    private final static IntWritable diff = new IntWritable(); // type of output value
    private IntWritable count = new IntWritable();   
    private IntWritable one = new IntWritable(1);                         // type of output key
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString(),"\n"); // line to string token
      while (itr.hasMoreTokens()) {
        String str = itr.nextToken();
        String [] tokens = str.split("\\t");
        count.set(Integer.parseInt(tokens[0]));
        diff.set(Integer.parseInt(tokens[1]));    
        context.write(diff, one);     
      }
   }
  }
     
      public static class FreqReducer
      extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
      private IntWritable result = new IntWritable();
      @Override
      public void reduce(IntWritable key, Iterable<IntWritable> values,Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
            for (IntWritable val : values) {
            
        	sum+=val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
   }

     
   public static void main(String[] args) throws Exception {
	    
    Configuration conf = new Configuration();
    Job job1 = Job.getInstance(conf, "job1");
    /* TODO: Needs to be implemented */

  
    
    job1.setJarByClass(Q4.class);
    job1.setMapperClass(DiffMapper.class);
    job1.setCombinerClass(DiffReducer.class);
    job1.setReducerClass(DiffReducer.class);
    job1.setOutputKeyClass(IntWritable.class);
    job1.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job1, new Path(args[0]));
    FileOutputFormat.setOutputPath(job1, new Path("outputQ4_31"));

    job1.waitForCompletion(true);

    Job job2 = Job.getInstance(conf, "job2");

    job2.setJarByClass(Q4.class);
    job2.setMapperClass(FreqMapper.class);
    job2.setCombinerClass(FreqReducer.class);
    job2.setReducerClass(FreqReducer.class);
    job2.setOutputKeyClass(IntWritable.class);
    job2.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job2, new Path("outputQ4_31"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    
     
    System.exit(job2.waitForCompletion(true) ? 0 : 1);


  }
}
