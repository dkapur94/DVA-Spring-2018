
package edu.gatech.cse6242;

import java.io.IOException;
import java.lang.Object;
import java.util.StringTokenizer;
import org.apache.hadoop.io.WritableComparator;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1b {

 public static class TokenizerMapper
       extends Mapper<Object, Text, Text, IntWritable>{

    private IntWritable weight = new IntWritable();
    private IntWritable email = new IntWritable();
    private IntWritable target = new IntWritable();
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString());
      while (itr.hasMoreTokens()) {
        String str = itr.nextToken();
        String [] tokens = str.split("\t");
        email.set(Integer.parseInt(tokens[0]));
        weight.set(Integer.parseInt(tokens[2]));
        target.set(Integer.parseInt(tokens[1]));
        context.write(email, weight);
      }
    }
   }   
      public class CompositeKey implements Writable,
  	WritableComparable<CompositeKey> {

	private IntWritable  receiver;
	private IntWritable weight;
	private IntWritable sender;


	public CompositeKey() {
	}


	public CompositeKey(IntWritable receiver, IntWritable weight, IntWritable sender) {
		this.receiver = receiver;
		this.sender = sender;
		this.weight = weight;
	}
  }
    @Override
        public int compareto(CompositeKey comp_key)
        {
            int compareValue = this.target.compareto(comp_key.getReciever()); 
            if (compareValue == 0)
            {
                compareValue = -1 * weight.compareto(comp_key.getWeight());
                if (comparevalue == 0)
                {
                    comparevalue = email.compareto(comp_key.getsender());
                }
            }
            return comparevalue;
        }

    
 @Override
        public boolean equals(Object o)
        {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;

            Compkeycl that = (Compkeycl) o;
            if (weight != null ? !weight.equals(that.weight) : that.weight != null) return false;
            if (email != null ? !email.equals(that.email) : that.email != null) return false;
            if (target != null ? !target.equals(that.target) : that.target != null) return false;

            return true;
        }

    }

   }
  

  public static class IntSumReducer
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
    private IntWritable result = new IntWritable();
    @Override
    public void reduce(IntWritable key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int max = 0;
      for (IntWritable val : values) {
        if(val.get()>max)
            max = val.get();
      }
      result.set(max);
      context.write(key, result);
    }
   }
  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1b");
    job.setJarByClass(Q1b.class);
    job.setOutputKeyClass(CompositeKey.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);
    /* TO DO: Needs to be implemented */
	
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
