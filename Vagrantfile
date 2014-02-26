# -*- mode: ruby -*-
# vi: set ft=ruby :

vm_ip                  = "172.94.43.181"
host_name              = "request.data.lo"

WINDOWS = (RbConfig::CONFIG['host_os'] =~ /mswin|mingw|cygwin/) ? true : false
vagrant_dir = File.dirname(__FILE__) + "/"

def chef(config, provider, hostname)
  config.vm.provision :chef_solo do |chef|

    chef.cookbooks_path = "cookbooks"
    # chef debug level, start vagrant like this to debug:
    # $ CHEF_LOG_LEVEL=debug vagrant <provision or up>
    chef.log_level = ENV['CHEF_LOG'] || "info"

    # chef recipes/roles
    chef.add_recipe("vagrant")

    chef.json = {
      :host_name => hostname,
      :user => "vagrant",
      :provider => provider,
    }
  end
end

Vagrant.configure("2") do |config|
  config.vm.provider :virtualbox do |provider, config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    config.vm.synced_folder ".", "/vagrant", :nfs => !WINDOWS

    provider.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]

    config.vm.network :private_network, ip: vm_ip
    config.vm.hostname = host_name

    chef(config, "virtualbox", host_name)
  end
end
