package com.novibe.common.base_structures;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.experimental.Accessors;

@EqualsAndHashCode(onlyExplicitlyIncluded = true)
@Accessors(fluent = true)
@Getter
public final class HostsLine {

    @EqualsAndHashCode.Include
    private final String domain;

    private final String ip;

    public HostsLine(String ip, String domain) {
        this.ip = ip;
        this.domain = domain;
    }

    public static HostsLine ipOnly(String ip) {
        return new HostsLine(ip, null);
    }

    public static HostsLine domainOnly(String domain) {
        return new HostsLine(null, domain);
    }

}