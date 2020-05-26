/* 
(c) 2007-2020 NIHPO, Inc.
Jose.Lacal@NIHPO.com - 26 May 2020

Purpose:
* This sample Java code connects with PHUSE's Open Data Repository ("PODR") and runs a couple of queries.
* Please keep in mind that you are only allowed 01 connection at the time to PODR's database.

If you are a PHUSE member: please contact Jose.Lacal@NIHPO.com to request a Username and Password to access PODR.

Requirements:
* Java 8+
* PostgreSQL's JDBC driver: download from https://jdbc.postgresql.org/download.html
* You must have these environment variables defined with the access details provided to you.
	"PHUSE_User"
	"PHUSE_Password"


To set environment variables:

In macOS:
	Open Terminal.
	export PHUSE_User="your assigned username here"
	export PHUSE_Password="your assigned password here"

In Windows:
	https://www.techjunkie.com/environment-variables-windows-10/


Process:
a.) Set environment variables.
b.) Compile this file: 
	javac -classpath postgresql-42.2.11.jar PHUSE_PODR.java
c.) run file:
	java -cp postgresql-42.2.11.jar:<Your local directory> PHUSE_PODR

*/
import java.sql.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.Map;
import java.util.Properties;
//
public class PHUSE_PODR {
	public static void main( String args[] ) {
		//
		System.out.println("Starting..");
		//
		// PostgreSQL constants:
		String pgsql_dbname = "nihpo";
		String pgsql_host = "podr.phuse.global";
		Integer pgsql_port = 5432;
		String pgsql_user = "";			// Value will be populated from environmental variable 'PHUSE_User'
		String pgsql_password = "";		// Value will be populated from environmental variable 'PHUSE_Password'
		//
		// Check for PostgreSQL's username and password in your environment:
		Map<String, String> env = System.getenv();
		//
		for (String envName : env.keySet()) {
			pgsql_user = env.get("PHUSE_User");
			pgsql_password = env.get("PHUSE_Password");
		}
		//
		if (pgsql_user == null) {
			System.out.println("\tPlease set the environment variable 'PHUSE_User'.");
			System.exit(0);
		}
		if (pgsql_password == null) {
			System.out.println("\tPlease set the environment variable 'PHUSE_Password'.");
			System.exit(0);
		}
		//
		try {
			// Reference: https://jdbc.postgresql.org/documentation/head/connect.html
			String url = "jdbc:postgresql://" + pgsql_host + ":" + pgsql_port + "/" + pgsql_dbname;	// "jdbc:postgresql://localhost/test";
			Properties props = new Properties();
			props.setProperty("user", pgsql_user);
			props.setProperty("password", pgsql_password);
			props.setProperty("ssl", "falsee");
			Connection con_nihpo_target = DriverManager.getConnection(url, props);
			//
			con_nihpo_target.setAutoCommit(false);
			System.out.println("\nConnected to PostgreSQL database :: [" + pgsql_dbname + "]");
			System.out.println("At host [" + pgsql_host + "] with port [" + pgsql_port + "]\n");
			//
			//
			// = = = Sample queries below = = =
			//
			//
			// 01. List all available tables:
			Statement stmt_01 = null;
			stmt_01 = con_nihpo_target.createStatement();
			ResultSet rs_01 = stmt_01.executeQuery("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';");
			System.out.println("\n\nList of all available tables in PODR:");
			while ( rs_01.next() ) { 
				String table_name = rs_01.getString("table_name");
				System.out.println(table_name);
				}
			rs_01.close();
			stmt_01.close();
			//
			//
			// 02. List 10 FDA Adverse Events for drug "IMURAN":
			Statement stmt_02 = null;
			stmt_02 = con_nihpo_target.createStatement();
			ResultSet rs_02 = stmt_02.executeQuery("SELECT caseid, cum_dose_chr, cum_dose_unit, dechal, dose_amt, dose_form, dose_freq, dose_unit, dose_vbm, drug_seq, drugname, exp_dt, lot_num, nda_num, primaryid, prod_ai, rechal, role_cod, route, val_vbm FROM nihpo_fda_aers_drug WHERE drugname = 'IMURAN' LIMIT 10;");
			System.out.println("\n\n10 Adverse Events from FDA's AERS, table 'nihpo_fda_aers_drug':");
			while ( rs_02.next() ) {
				// 
				String caseid = rs_02.getString("caseid");
				String cum_dose_chr = rs_02.getString("cum_dose_chr");
				String cum_dose_unit = rs_02.getString("cum_dose_unit");
				String dechal = rs_02.getString("dechal");
				String dose_amt = rs_02.getString("dose_amt");
				String dose_form = rs_02.getString("dose_form");
				String dose_freq = rs_02.getString("dose_freq");
				String dose_unit = rs_02.getString("dose_unit");
				String dose_vbm = rs_02.getString("dose_vbm");;
				String drug_seq = rs_02.getString("drug_seq");
				String drugname = rs_02.getString("drugname");
				String exp_dt = rs_02.getString("exp_dt");
				String lot_num = rs_02.getString("lot_num");
				String nda_num = rs_02.getString("nda_num");
				String primaryid = rs_02.getString("primaryid");
				String prod_ai = rs_02.getString("prod_ai");
				String rechal = rs_02.getString("rechal");
				String role_cod = rs_02.getString("role_cod");
				String route = rs_02.getString("route");
				String val_vbm = rs_02.getString("val_vbm");
				/*
				float <..>  = rs.getFloat("<..> ");
				int <..>  = rs.getInt("<..> ");
				String <..>  = rs.getString("<..> ");
				*/
				System.out.println( caseid + " :: " + cum_dose_chr + " :: " + cum_dose_unit + " :: " + dechal + " :: " + dose_amt + " :: " + dose_form + " :: " + dose_freq + " :: " + dose_unit + " :: " + dose_vbm + " :: " + drug_seq + " :: " + drugname + " :: " + exp_dt + " :: " + lot_num + " :: " + nda_num + " :: " + primaryid + " :: " + prod_ai + " :: " + rechal + " :: " + role_cod + " :: " + route + " :: " + val_vbm);
			}
			rs_02.close();
			stmt_02.close();
			con_nihpo_target.close();
			System.out.println("You disconnected from the PHUSE PODR database.");
			//
		} catch ( Exception e ) {
			System.out.println("There was an error connecting to PHUSE's Open Data Repository.");
			System.err.println( e.getClass().getName()+": "+ e.getMessage() );
			System.exit(0);
		}
   }
}
