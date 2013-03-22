# Sominst

*Ppackaging tool using python 2.6.6 or above to create a project pacakge and install and deploy it*

The tool uses .sicf file extension for the project definition.

   1. [Usage](#usage)
   1. [Current Implementation](#implementation)

## <a name='usage'>Usage</a>

   - **Sample sicf**

   ```text
   #########################################################################
   ## meta data
   #########################################################################
   meta project news_spiders
   meta version $(version)
   meta description News spider script

   #########################################################################
   ## variables to replace token in files
   #########################################################################
   set host locahost
   set port 80
   set dbhost locahost
   set dbhostport 3306

   #########################################################################
   ## internal variables
   #########################################################################
   var src_dir src
   var dest_dir /usr/bin
   var version 0.0.1

   #########################################################################
   ## directories
   #########################################################################
   dir - - - $(dest_dir)

   #########################################################################
   ## assets
   #########################################################################
   find - - - $(src_dir) $(dest_dir)
               
   #########################################################################
   ## files
   #########################################################################

   #########################################################################
   ## post action
   #########################################################################
   ```

